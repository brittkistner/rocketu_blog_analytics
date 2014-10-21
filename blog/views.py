from django.shortcuts import render, get_object_or_404
from blog.models import Post


def blog(request):
    return render(request, 'blog.html', {
        'posts': Post.objects.order_by('-created')
    })


def post(request, pk):
    post_obj = get_object_or_404(Post, pk=pk)
    # try:
    #     post_obj = Post.objects.get(pk=pk)
    # except Post.DoesNotExist:
    #     pass

    return render(request, 'post.html', {
        'post': post_obj
    })

def list_posts(request, tag_id):
    #don't forget about get_object_or_404
    #list all posts here associated with a tag id
    return render (request, 'blog_list.html', {
        'posts': Post.objects.filter(tags__pk=tag_id)
    })


