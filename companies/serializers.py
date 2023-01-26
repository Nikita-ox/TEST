from rest_framework import serializers

from .models import Company, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    def validate(self, data):
        instance = self.instance
        if instance:
            original_debt = instance.debt
            new_debt = data.get('debt')

            if new_debt and (new_debt != original_debt):
                data.update({'debt': original_debt})
        return data

    products = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class CompanyQRSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    country = serializers.CharField()
    city = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.CharField()

    class Meta:
        model = Product
        fields = ('name', 'email', 'country', 'city', 'street', 'house_number')
