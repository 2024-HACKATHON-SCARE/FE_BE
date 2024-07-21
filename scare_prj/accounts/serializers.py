from rest_framework import serializers
from accounts.models import User, Follow

class FollowSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all()
    )
    to_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    status = serializers.CharField(read_only=True)

    def validate(self, data):
        from_user = data['from_user']
        to_user = data['to_user']

        if from_user == to_user:
            raise serializers.ValidationError("자기 자신에게 친구 신청할 수 없습니다.")

        if from_user.followers.filter(id=to_user.id).exists():
            raise serializers.ValidationError("이미 친구입니다.")

        if from_user.sent_follow_requests.filter(to_user=to_user).exists():
            raise serializers.ValidationError("이미 친구신청을 보냈습니다.")

        return data

    def create(self, validated_data):
        follow_request = Follow.objects.create(
            from_user=validated_data['from_user'],
            to_user=validated_data['to_user'],
            status='pending'
        )
        return follow_request

    class Meta:
        model = Follow
        fields = '__all__'
