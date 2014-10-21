from datetime import datetime
from localflavor.us.us_states import STATES_NORMALIZED
from blog.models import Post, Tag, AdImage

def latest_post(request):
    return {
        'latest_post':Post.objects.latest('created'),
    }

# list of all tags in db and the number of posts which have been tagged with this tag

def list_tags(request):
    return {
        'tags': Tag.objects.all(),
    }

def list_years_months(request):
    # post_dates = Post.objects.order_by('-created')
    return {

    }


def random_ad(request):
    # state = request.location['region'].lower()
    # print state
    # location = STATES_NORMALIZED[state]
    # print location

    return {
        'random_image' : AdImage.objects.filter(state=request.location['region']).order_by('?').first()
        # 'random_image' : AdImage.objects.filter(state=location).order_by('?').first()
    }