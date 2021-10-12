from django.conf import settings
from django.db import models
from django.contrib import admin
import requests

# Create your models here.
class Request(models.Model):
    REQUEST_CHOICES = (('Incident', 'Incident'), ('Create Resource', 'Create Resource'), ('Change Resource', 'Change Resource'), ('Delete Resource', 'Delete Resource'))
    PRIORITY_CHOICES = (('1 - Critical', '1 - Critical'), ('2 - High', '2 - High'), ('3 - Medium', '3 - Medium'), ('4 - Low', '4 - Low'))

    req_title    = models.CharField('Request Title', max_length=100)
    req_type     = models.CharField('Request Type', max_length=50, choices=REQUEST_CHOICES)
    req_priority = models.CharField('Priority', max_length=50, choices=PRIORITY_CHOICES, default='4 - Low')
    req_sent     = models.BooleanField('GitLab Created', default=False, blank=True, null=True)
    req_body     = models.TextField('Request Description', blank=True, null=True)
    requester    = models.ForeignKey('custom_user.User', blank=True, null=True, on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = 'Support Request'
        verbose_name_plural = 'Support Requests'    

    def __str__(self):
        return str(self.req_type) + ' ' + str(self.id)

    def save(self):
        """
            Overwrites the default save() method including 
            custom logic before saving the model object.

            In this case, the save() method insert an issue in gitlab 
            waiting for a 200|201 response code as success indicator.

            It also post a messa in a given MS Teams channel.
        """

        print(f"ln 36, Item ID: {self.id}")

        url_gitlab      = f"{settings.GITLAB_URL}/issues?title={self.req_title}&type={self.req_type}&description={self.req_body}&labels={self.req_priority}"
        headers_gitlab  = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'PRIVATE-TOKEN': settings.PRIVATE_TOKEN}
        response_gitlab = requests.post(url=url_gitlab, headers=headers_gitlab, json='')
        
        print(f"ln 42, Git Lab Request Status Code: {response_gitlab.status_code}")

        if response_gitlab.status_code == 200 or response_gitlab.status_code == 201:
            self.req_sent = True
            print(f"Issue Url: {response_gitlab.json()['web_url']}")
            print(f"Issue iID: {response_gitlab.json()['iid']}")

        url_teams  = settings.MS_TEAMS_WEBHOOK
        data_teams = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "New Support Request Sent",
            "sections": [{
                "activityTitle": "New Support Request Sent",
                "activitySubtitle": "As GitLab Issue",
                "activityImage": "https://st3.depositphotos.com/8950810/17657/v/600/depositphotos_176577870-stock-illustration-cute-smiling-funny-robot-chat.jpg",
                "facts": [{
                    "name": "Service",
                    "value": "New Service Request Created"
                }, {
                    "name": "Request Title",
                    "value": f"{self.req_title}"
                },
                {
                    "name": "Priority",
                    "value": f"{self.req_priority}"
                },
                 {
                    "name": "Requester",
                    "value": f"{self.requester}"
                }, {
                    "name": "Description",
                    "value": f"{self.req_body}"
                }, {
                    "name": "Status",
                    "value": "Created / New"
                }],
                "markdown": "true"
            }],
            "potentialAction": [ {
                "@type": "OpenUri",
                "name": "See/Check the Service Request",
                "targets": [{
                    "os": "default",
                    "uri": f"{response_gitlab.json()['web_url']}"
                }]
            }]
        }

        headers  = { 'Accept': 'application/json', 'Content-Type': 'application/json' }
        response = requests.post(url=url_teams, headers=headers, json=data_teams)
        print(f"ln 94, response status code: {response.status_code}")

        """
        If you want to include more logic, include it until super().save() method.
        """
        
        super().save()

class RequestAdmin(admin.ModelAdmin):
    list_display  = ('id', 'req_title', 'req_type')
    search_fields = ('req_title', 'req_sent')
    list_filter   = ('req_title', 'req_sent', 'req_type')
    readonly_fields  = ('requester', 'req_sent',)

    

