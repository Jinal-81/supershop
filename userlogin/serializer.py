from rest_framework import serializers

from userlogin.models import MyUser, Address


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the user."""
    confirm_password = serializers.CharField(label='Confirm Password', required=False, allow_null=True, write_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api_user_retrieve")
    # fullname = serializers.SerializerMethodField()
    # full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = MyUser
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'mobile_number','password', 'confirm_password',
                  'profile_pic']
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'password': {'write_only': True}
        }  # when we don't need to print this fields in result

    def to_representation(self, instance):
        """when we need to change api result in custom format."""
        representation = super().to_representation(instance) # pass instance to the to_representation method so return orderqueryset.
        return {'full_name': instance.first_name.upper() + " " + instance.last_name.upper(), **representation} # return orderdictionry with the fullname.

    # def to_representation(self, value):
    #     # duration = time.strftime('%M:%S', time.gmtime(value.duration))
    #     return '%s %s' % (value.first_name.upper(), value.last_name.upper())
    #     # import pdb; pdb.set_trace()

    # def get_full_name(self, obj):
    #     """form firstname and last name into fullname."""
    #     return obj.first_name.upper() + " " + obj.last_name.upper()

    def validate_first_name(self, value):
        """validate that firstname is only character."""
        if not value.isalpha():
            raise serializers.ValidationError("Please enter only character!!")
        return value

    def validate(self, attrs):
        """validate password and confirm password is same."""
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("password and confirm password should be same!!")

        elif attrs.get('password') == attrs.get('confirm_password'):
            attrs.pop('confirm_password')
        return attrs


class UserSerializerV1(serializers.ModelSerializer):
    """serializer for the username only using versioning."""

    class Meta:
        model = MyUser
        fields = ['username', ]


class AddressSerializer(serializers.ModelSerializer):
    """serializer for address."""

    class Meta:
        model = Address
        fields = '__all__'


class AddressSerializerV1(serializers.ModelSerializer):
    """serializer for the city only using versioning."""

    class Meta:
        model = Address
        fields = ['city', ]


class EmailVerificationSerializer(serializers.ModelSerializer):
    """serializer for email and code verification."""
    code = serializers.IntegerField()
    email = serializers.EmailField()
    newPassword = serializers.CharField()

    class Meta:
        model = MyUser
        fields = ['email', 'code', 'newPassword', ]


class CodeSerializer(serializers.Serializer):
    """serializer for token generate"""
    email = serializers.EmailField()

    class Meta:
        model = MyUser
        fields = ['email']
