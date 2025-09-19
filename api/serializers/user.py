import random
from rest_framework import serializers
from api.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(required=True, allow_blank=False)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, default='member')
    phone_number = serializers.CharField(required=False, allow_blank=True)
    document = serializers.FileField(required=False, allow_null=True)
    picture = serializers.ImageField(required=False, allow_null=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'full_name', 'role', 
            'phone_number', 'document', 'picture', 'username'
        ]

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
    
    def validate(self, attrs):
        request = self.context.get('request')
        creator = request.user if request and request.user.is_authenticated else None
        role = attrs.get('role', 'member')

        if role in ['admin', 'superadmin']:
            if not creator or creator.role != 'superadmin':
                raise serializers.ValidationError({
                    'role': "Only superadmins can assign 'admin' or 'superadmin' roles."
                })
        return attrs
    
    def generate_username(self, email):
        base_username = email.split('@')[0]
        while CustomUser.objects.filter(username=base_username).exists():
            base_username += str(random.randint(1, 9999))
        return base_username

    def validate_username(self, value):
        if CustomUser.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        request = self.context.get('request', None)
        creator = request.user if request and request.user.is_authenticated else None

        if creator and creator.role == 'admin':
            validated_data['role'] = 'member'

        full_name = validated_data.pop('full_name')
        phone_number = validated_data.pop('phone_number', '')
        document = validated_data.pop('document', None)
        picture = validated_data.pop('picture', None)

        # ✅ Properly get or generate username
        username = validated_data.get('username') or self.generate_username(validated_data['email'])

        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
        )

        user.full_name = full_name
        user.role = validated_data.get('role', 'member')
        user.phone_number = phone_number
        if document:
            user.document = document
        if picture:
            user.picture = picture
        user.save()

        return user

