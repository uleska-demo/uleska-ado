#!/usr/bin/env python3

import json
import sys
import requests
import argparse



def _main():

    #Capture command line arguments
    arguments = sys.argv

    #Capture command line arguments
    arg_options = argparse.ArgumentParser(description="Uleska ADO Work Item Generator. (Version 0.1)", )
    arg_options.add_argument('--host', help="Azure DevOps host to communicate with (e.g. dev.azure.com", required=True, type=str)
    arg_options.add_argument('--organization', help="Organization string", required=True, type=str)
    arg_options.add_argument('--project', help="Project string", required=True, type=str)
    arg_options.add_argument('--token', help="Personal access token string (base64 encoded with username)", required=True, type=str)
    arg_options.add_argument('--filename', help="File to read Uleska issues from, defaults to 'output.json'", type=str)


    args = arg_options.parse_args()

    host = ""
    organization = ""
    project = ""
    token = ""
    filename = "output.json"

    debug = True

    #Grab the host from the command line arguments
    if args.host is not None:
        host = args.host

        if debug:
            print("Host: " + host)

    #Grab the org from the command line arguments
    if args.organization is not None:
        organization = args.organization

        if debug:
            print("Organization: " + organization)

    #Grab the project from the command line arguments
    if args.project is not None:
        project = args.project

        if debug:
            print("Project: " + project)

    #Grab the token from the command line arguments
    if args.token is not None:
        token = args.token

        if debug:
            print("Token: " + token)

    #Grab the filename from the command line arguments
    if args.filename is not None:
        filename = args.filename

        if debug:
            print("Filename: " + filename)



    #https://dev.azure.com/anaeko-azure/Anaeko-WHOProject/_apis/wit/workitems/$Bug?api-version=6.0
    # URL for your org
    url = "https://" + host + "/" + organization + "/" + project + "/_apis/wit/workitems/$Bug?api-version=6.0"

    if debug:
        print ("Url is " + url)


    s = requests.Session()

    s.headers.update({
        'Content-Type': "application/json-patch+json",
        'cache-control': "no-cache",
        'Authorization': "Basic " + token
        })


    # Open and Load JSON file

    j = open(filename)
    jdata = json.load(j)

    # Loop through all new issues
    for i in jdata['new_issues']:
        # Issue details
        payload = '[{"op": "add", "path": "/fields/System.Title", "from": null, "value": "' + i['title'] + '"},{"op": "add", "path": "/fields/Microsoft.VSTS.TCM.ReproSteps", "from": null, "value": "<b>Summary:</b> ' +  i['summary'] + '<div><div><b>Explanation:</b> ' + i['explanation'] + '<div><div><b>Tool:</b> ' + i['tool'] + '<div><div><b>Recommendation</b> ' + i['recommendation'] + '"}]'


        print ("Payload: " + payload + "\n")

        payload_json = json.loads(payload)

        try:
            StatusResponse = s.request("POST", url, json=payload_json)
        except requests.exceptions.RequestException as err:
            print ("Exception raising ADO work item\n" + str(err))
            sys.exit(2)

        if StatusResponse.status_code != 200:
            #Something went wrong, maybe server not up, maybe auth wrong
            print("Non 200 status code returned when getting applications and versions.  Code [" + str(StatusResponse.status_code) + "] Body [" + str(StatusResponse.text) + "]")
            sys.exit(2)



if __name__ == "__main__":
    _main()

