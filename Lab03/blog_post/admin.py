from django.contrib import admin
# Register your models here.
from .models import BlogUser,PostComment,Post,Block

class BlogUserAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permissiongUser(self, request, obj=None):
        return obj is not None and request.user == obj.user

    def has_delete_permission(self, request, obj=None):
        return obj is not None and request.user == obj.user

    def has_add_permission(self, request):
        return request.user.is_superuser


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    search_fields = ["title", "content"]
    list_filter = ["created_on"]
    exclude = ["author"]

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or (obj is not None and not Block.objects.filter(blocker__user=obj.author.user,
                                                                                          blocked__user=request.user).exists())

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj is not None and request.user == obj.author.user)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or (obj is not None and request.user == obj.author.user)

    def has_add_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        if obj is not None:
            obj.author = BlogUser.objects.get(user=request.user)

        super().save_model(request, obj, form, change)


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ["content", "created_on"]
    exclude = ["author"]

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or (
                obj is not None and not Block.objects.filter(blocker__user=obj.post.author.user,
                                                             blocked__user=request.user).exists())

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj is not None and request.user == obj.author.user)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or (
                obj is not None and (request.user == obj.post.user or request.user == obj.author.user))

    def has_add_permission(self, request):
        return True

    def save_model(self, request, obj, form, change):
        if obj is not None:
            obj.auhor = BlogUser.objects.get(user=request.user)

        super().save_model(request, obj, form, change)


class BlockAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return obj is not None and request.user == obj.blocker.user

    def has_delete_permission(self, request, obj=None):
        return obj is not None and request.user == obj.blocker.user

    def has_add_permission(self, request):
        return True


admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Block, BlockAdmin)
