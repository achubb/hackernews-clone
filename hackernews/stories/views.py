import datetime

from django.shortcuts import render

from django.template import loader, Context
from stories.models import Story
from django.utils.timezone import utc
from django.http import HttpResponse

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
	# Use the django.template loader module to load in the template 
	template = loader.get_template("stories/index.html")
	# Create the context for the template - i.e variables associated
	context = Context({'stories': stories})
	# Render the template out - passing in the context
	response = template.render(context)
	return HttpResponse(response)