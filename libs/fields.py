from rest_framework import serializers
from rest_framework.relations import ManyRelatedField
from versatileimagefield.utils import get_url_from_image_key


class ImageFieldSerializer(serializers.ImageField):
    def __init__(self, size, *args, mode="crop", **kwargs):
        self.mode = mode
        self.size = size

        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        value: the image to transform
        returns: a url pointing at a scaled image
        """
        if not value:
            return None

        image = getattr(value, self.mode)[self.size]

        try:
            request = self.context.get("request", None)
            return request.build_absolute_uri(image.url)
        except:
            try:
                return super().to_representation(image)
            except AttributeError:
                return super().to_native(image.url)

    to_native = to_representation


class ImageKeySerializer(serializers.ImageField):
    def __init__(self, key, *args, **kwargs):
        self.key = key
        kwargs["read_only"] = True
        super().__init__(*args, **kwargs)

    def get(self, value, key_name, request):
        try:
            key = value.instance.SIZES[value.field.name][key_name]
        except KeyError:
            return
        url = get_url_from_image_key(value, key)
        # url = url.replace('%2520', '%20')

        if "%2520" in url:
            return None

        if request:
            return request.build_absolute_uri(url)
        else:
            try:
                rep = super().to_representation(url)
                if rep is None:
                    return url
                return rep
            except AttributeError:
                return super().to_native(url)

    def to_representation(self, value):
        if not value:
            return None
        request = self.context.get("request", None)
        if type(self.key) == str:
            return self.get(value, self.key, request)
        elif type(self.key) == list:
            urls = {}
            for key_name in self.key:
                urls[key_name] = self.get(value, key_name, request)
            return urls
        else:
            raise ValueError("Key must be either string or a list.")

    to_native = to_representation


def many_to_internal_value(self, data):
    if data == ["null"]:
        data = []
    if isinstance(data, str) or not hasattr(data, "__iter__"):
        self.fail("not_a_list", input_type=type(data).__name__)
    if not self.allow_empty and len(data) == 0:
        self.fail("empty")

    return [self.child_relation.to_internal_value(item) for item in data]


ManyRelatedField.to_internal_value = many_to_internal_value


class EmptyForNullTextField(serializers.CharField):
    def get_attribute(self, instance):
        attibute = super().get_attribute(instance)
        if attibute is None:
            attibute = ""
        return attibute
