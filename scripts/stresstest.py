import json
import os
import random
from locust import HttpLocust, TaskSet, task

class SimpleLocustTest(TaskSet):

    original_synonyms = [
        "cyber espionage, nation state espionage, corporation espionage, financial espionage, targeted attacks, denial and deception",
        "vulnerabilities, zero-day, 0-day, exploitation, hardware vulnerabilities, software vulnerabilities",
        "information leakage, misconfiguration, data leaks, personal data",
        "phishing, social engineering, spear-phishing, malware, spam, data stealing",
        "identity theft, social engineering, social media abuse, dark web shopping, confidential information, sensitive information, impersonation, credential stealing, personal information, personal data",
        "data breaches, personal data, exploitation, hacking, security vulnerabilities, security incident, credential theft, data dump",
        "malware, advanced persistent threat, apt, virus, worm, ransomware, trojan, cryptominer, rootkit, bootkit, backdoor, spyware, scareware, addware, keylogger",
        "exploit kits, vulnerabilities, zero-day, 0-day",
        "spam, social engineering, malware",
        "web application attacks, cross-site scripting, xss, local file inclusion, lfi, remote file inclusion, rfi, sql injection, cross-site request forgery, csrf",
        "botnets, ddos, iot botnet",
        "denial of service, amplification attacks, reflection attacks",
        "physical manipulation damage, outage, failures, malfunction, environmental disaster, natural disaster, physical attack, damage caused by third party",
        "web based attacks, drive-by downloads, cryptojacking, man-in-the-browser, waterholing, supply-chain attack",
        "insider threat, human error, malicious insider, cyber espionage, un-authorised access, data leak",
        "threats, cyber espionage, nation state espionage, corporation espionage, financial espionage, targeted attacks, denial and deception, vulnerabilities, zero-day, 0-day, exploitation, hardware vulnerabilities, software vulnerabilities, information leakage, misconfiguration, data leaks, personal data, phishing, social engineering, spear-phishing, malware, spam, data stealing, identity theft, social engineering, social media abuse, dark web shopping, confidential information, sensitive information, impersonation, credential stealing, personal information, personal data, data breaches, personal data, exploitation, hacking, security vulnerabilities, security incident, credential theft, data dump, malware, advanced persistent threat, apt, virus, worm, ransomware, trojan, cryptominer, rootkit, bootkit, backdoor, spyware, scareware, addware, keylogger, exploit kits, vulnerabilities, zero-day, 0-day, spam, social engineering, malware, web application attacks, cross-site scripting, xss, local file inclusion, lfi, remote file inclusion, rfi, sql injection, cross-site request forgery, csrf, botnets, ddos, iot botnet, denial of service, amplification attacks, reflection attacks, physical manipulation damage, outage, failures, malfunction, environmental disaster, natural disaster, physical attack, damage caused by third party, web based attacks, drive-by downloads, cryptojacking, man-in-the-browser, waterholing, supply-chain attack, insider threat, human error, malicious insider, cyber espionage, un-authorised access, data leak"                
    ]

    splitted_synonyms = [i.split(',') for i in original_synonyms]
    words = [item for sublist in splitted_synonyms for item in sublist]

    # words = ["malware", "technology", "trump", "security", "facebook", 
    # "intel", "threat", "hacks", "web", "cryptography", "risk", "europe",
    # "iot", "data", "russia", "android", "google", "browser"]

    def request(self):
        body = {
            "size": 50,
            "sort": [
                {
                    "_score": {
                        "order": "desc"
                    }
                }
            ],
            "_source": {
                "excludes": []
            },
            "stored_fields": [
                "*"
            ],
            "script_fields": {},
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": random.choice(self.words),
                                "analyze_wildcard": "true",
                                "default_field": "*"
                            }
                        }
                    ],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            }
        }
        return json.dumps(body)


    @task
    def get_something(self):
        es_index = os.environ.get("ES_INDEX")
        self.client.post("/" + es_index + "/_search", data=self.request(),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'})

class LocustTests(HttpLocust):
    task_set = SimpleLocustTest