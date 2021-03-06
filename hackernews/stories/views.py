import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required

from stories.models import Story
from stories.forms import StoryForm

def score(story, gravity=1.8, timebase=120):
	# Calculate the points for the story
	points = (story.points -1)**0.8
	# Figure out the age of the story
	now = datetime.datetime.utcnow().replace(tzinfo=utc)
	age = int((now - story.created_at).total_seconds())/60
	return points/(age+timebase)**1.8

def top_stories(top=180, consider=1000):
	# Figure out what the latest stories are
	latest_stories = Story.objects.all().order_by('-created_at')[:consider]
	# Rank the stories - loop throught latest stories, get each score and each story, then sore them in the order best to worst
	# or highest scored to lowest scored
	ranked_stories = sorted([(score(story), story) for story in latest_stories], reverse=True)
	# Return the stories as defined in top, lose the score as that is not needed now
	return [story for _, story in ranked_stories][:top]

def index(request):
	# Get a list of all the top stories and store them in the stories var
	stories = top_stories(top=30)
	if request.user.is_authenticated():
		liked_stories = request.user.liked_stories.filter(id__in=[story.id for story in stories])
	else:
		liked_stories = []
	return render(request, 'stories/index.html', {
		'stories': stories,
		'user': request.user,
		'liked_stories': liked_stories,
	})

@login_required
def story(request):
	# Check to see if the form has been posted or not
	if request.method == 'POST':
		# Create a bound form object by passing the posted data through. 
		form = StoryForm(request.POST)
		if form.is_valid():
			story = form.save(commit=False)
			story.moderator = request.user
			story.save()
			return HttpResponseRedirect('/')
	else :
		# Otherwise just create an unbound form - creates the HTML for the form and sends that back
		form = StoryForm()
	return render(request, 'stories/story.html', {'form': form})

@login_required
def vote(request):
	story = get_object_or_404(Story, pk=request.POST.get('story'))
	story.points += 1
	story.save()
	user = request.user
	user.liked_stories.add(story)
	user.save()
	return HttpResponse()