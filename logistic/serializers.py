from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=50)

    class Meta:
        model = Product
        fields = ['title', 'description']



class ProductPositionSerializer(serializers.ModelSerializer):
    products = serializers.CharField(max_length=200)
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']
    # настройте сериализатор для позиции продукта на складе


class StockSerializer(serializers.ModelSerializer):
    # products = serializers.CharField(max_length=200)
    # positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        for el in positions:
            StockProduct.objects.create(stock=stock, **el)
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for el in positions:
            obj, created = StockProduct.objects.update_or_create(stock=stock,
                                                                 product=el['product'],
                                                                 defaults={'stock': stock, 'product': el['product'], 'quantity': el['quantity'], 'price': el['price']})

        return stock
