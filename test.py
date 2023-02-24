import requests
import time

unique_id = ""
username = ""
password = ""

search_query = 'search index="main" source = tutorialdata.zip:./vendor_sales/vendor_sales.log | table host, VendorID, Code, AcctID'

post_data = {
            'id': unique_id,
            'max_count': '200',
            'search': search_query,
            'earliest_time': '-24',
            'latest_time': 'now'
            }

splunk_search_base_url = 'https://192.168.1.200:8089/servicesNS/{}/search/search/jobs'.format(username)
resp = requests.post(splunk_search_base_url, data=post_data, verify=False, auth=(username, password))
print(resp.text)

is_job_completed = ''

while(is_job_completed != 'DONE'):
    time.sleep(1)
    get_data = {'output_mode': 'json'}
    job_status_base_url = 'https://192.168.1.200:8089/servicesNS/{}/search/search/jobs/{}'.format(username, unique_id)
    resp_job_status = requests.post(job_status_base_url, data=get_data, verify=False, auth=(username, password))
    resp_job_status_data = resp_job_status.json()
    is_job_completed = resp_job_status_data['entry'][0]['content']['dispatchState']
    print("Current Job Status is {}".format(is_job_completed))

splunk_summary_base_url = 'https://192.168.1.200:8089/servicesNS/{}/search/search/jobs/{}/results'.format(username, unique_id)
splunk_summary_results = requests.get(splunk_search_base_url, data=get_data, verify=False, auth=(username, password))
print(splunk_summary_results.text)
splunk_summary_data = splunk_summary_results.json()

print(splunk_summary_data)
# for data in splunk_summary_data['results']:
#     print(data)