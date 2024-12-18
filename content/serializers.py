from rest_framework import serializers

from content.models import Book,Kind,Form,Matter,Author,PublishingHouse,UserProfile

class KindSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
         # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model=Kind
        fields="__all__"

class FormSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
         # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model=Form
        fields="__all__"

class MatterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
         # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model=Matter
        fields="__all__"

class AuthorSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
         # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model=Author
        fields="__all__"

class PublishingHouseSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
         # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model=PublishingHouse
        fields="__all__"

class BookSerializers(serializers.ModelSerializer):

    def create(self, validated_data):
         # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    kind_FK=KindSerializer(read_only=True)
    kind_FK_id=serializers.PrimaryKeyRelatedField(queryset=Kind.objects.all(),write_only=True,source="kind_FK")
    
    author_FK=AuthorSerializer(read_only=True)
    author_FK_id=serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),write_only=True,source="author_FK")
    
    matter_FK=MatterSerializer(read_only=True)
    matter_FK_id=serializers.PrimaryKeyRelatedField(queryset=Matter.objects.all(),write_only=True,source="matter_FK")
    
    form_FK=FormSerializer(read_only=True)
    form_FK_id=serializers.PrimaryKeyRelatedField(queryset=Form.objects.all(),write_only=True,source="form_FK")
    
    publishingHouse_FK=PublishingHouseSerializer(read_only=True)
    publishingHouse_FK_id=serializers.PrimaryKeyRelatedField(queryset=PublishingHouse.objects.all(),write_only=True,source="publishingHouse_FK")

    class Meta:
        model = Book
        fields="__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "opt_key"]

        