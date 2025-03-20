# Copyright 2022 David Harcombe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import dataclasses
from typing import Optional

import aenum as enum
import dataclasses_json
import immutabledict

from . import camel_field, lazy_property


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class ServiceDefinition(object):
  """Defines a Google Service for the builder."""
  service_name: Optional[str] = camel_field()
  version: Optional[str] = camel_field()
  discovery_service_url: Optional[str] = camel_field()


class S(enum.Enum):
  """Defines the generic Enum for any service.

  Raises:
      ValueError: if no enum is defined.
  """
  @lazy_property
  def definition(self) -> ServiceDefinition:
    """Fetch the ServiceDefinition.

    Lazily returns the dataclass containing the service definition
    details. It has to be lazy, as it can't be defined at
    initialization time.

    Returns:
        ServiceDefinition: the service definition
    """
    (service_name, version) = SERVICE_DEFINITIONS.get(self.name)
    return ServiceDefinition(
        service_name=service_name,
        version=version,
        discovery_service_url=(
            f'https://{service_name}.googleapis.com/$discovery/rest'
            f'?version={version}'))

  @classmethod
  def from_value(cls, value: str) -> S:
    """Creates a service enum from the name of the service.

    Args:
        value (str): the service name

    Raises:
        ValueError: no service found

    Returns:
        S: the service definition
    """
    for k, v in cls.__members__.items():
      if k == value.upper():
        return v
    else:
      raise ValueError(f"'{cls.__name__}' enum not found for '{value}'")


SERVICE_DEFINITIONS = \
    immutabledict.immutabledict(
        {'ABUSIVEEXPERIENCEREPORT': ('abusiveexperiencereport', 'v1'),
         'ACCELERATEDMOBILEPAGEURL': ('acceleratedmobilepageurl', 'v1'),
         'ACCESSAPPROVAL': ('accessapproval', 'v1'),
         'ACCESSCONTEXTMANAGER': ('accesscontextmanager', 'v1'),
         'ADDRESSVALIDATION': ('addressvalidation', 'v1'),
         'ADEXCHANGEBUYER2': ('adexchangebuyer2', 'v2beta1'),
         'ADEXPERIENCEREPORT': ('adexperiencereport', 'v1'),
         'ADMIN': ('admin', 'reports_v1'),
         'ADMOB': ('admob', 'v1'),
         'ADSENSE': ('adsense', 'v2'),
         'ADSENSEPLATFORM': ('adsenseplatform', 'v1'),
         'ADVISORYNOTIFICATIONS': ('advisorynotifications', 'v1'),
         'AIPLATFORM': ('aiplatform', 'v1'),
         'AIRQUALITY': ('airquality', 'v1'),
         'ALERTCENTER': ('alertcenter', 'v1beta1'),
         'ALLOYDB': ('alloydb', 'v1'),
         'ANALYTICS': ('analytics', 'v3'),
         'ANALYTICSADMIN': ('analyticsadmin', 'v1beta'),
         'ANALYTICSDATA': ('analyticsdata', 'v1beta'),
         'ANALYTICSHUB': ('analyticshub', 'v1'),
         'ANALYTICSREPORTING': ('analyticsreporting', 'v4'),
         'ANDROIDDEVICEPROVISIONING': ('androiddeviceprovisioning', 'v1'),
         'ANDROIDENTERPRISE': ('androidenterprise', 'v1'),
         'ANDROIDMANAGEMENT': ('androidmanagement', 'v1'),
         'ANDROIDPUBLISHER': ('androidpublisher', 'v3'),
         'APIGATEWAY': ('apigateway', 'v1'),
         'APIGEE': ('apigee', 'v1'),
         'APIGEEREGISTRY': ('apigeeregistry', 'v1'),
         'APIKEYS': ('apikeys', 'v2'),
         'APIM': ('apim', 'v1alpha'),
         'APPENGINE': ('appengine', 'v1'),
         'APPHUB': ('apphub', 'v1'),
         'AREA120TABLES': ('area120tables', 'v1alpha1'),
         'AREAINSIGHTS': ('areainsights', 'v1'),
         'ARTIFACTREGISTRY': ('artifactregistry', 'v1'),
         'ASSUREDWORKLOADS': ('assuredworkloads', 'v1'),
         'AUTHORIZEDBUYERSMARKETPLACE': ('authorizedbuyersmarketplace', 'v1'),
         'BACKUPDR': ('backupdr', 'v1'),
         'BAREMETALSOLUTION': ('baremetalsolution', 'v2'),
         'BATCH': ('batch', 'v1'),
         'BEYONDCORP': ('beyondcorp', 'v1'),
         'BIGLAKE': ('biglake', 'v1'),
         'BIGQUERY': ('bigquery', 'v2'),
         'BIGQUERYCONNECTION': ('bigqueryconnection', 'v1'),
         'BIGQUERYDATAPOLICY': ('bigquerydatapolicy', 'v1'),
         'BIGQUERYDATATRANSFER': ('bigquerydatatransfer', 'v1'),
         'BIGQUERYRESERVATION': ('bigqueryreservation', 'v1'),
         'BIGTABLEADMIN': ('bigtableadmin', 'v2'),
         'BILLINGBUDGETS': ('billingbudgets', 'v1'),
         'BINARYAUTHORIZATION': ('binaryauthorization', 'v1'),
         'BLOCKCHAINNODEENGINE': ('blockchainnodeengine', 'v1'),
         'BLOGGER': ('blogger', 'v3'),
         'BOOKS': ('books', 'v1'),
         'BUSINESSPROFILEPERFORMANCE': ('businessprofileperformance', 'v1'),
         'CALENDAR': ('calendar', 'v3'),
         'CERTIFICATEMANAGER': ('certificatemanager', 'v1'),
         'CHAT': ('chat', 'v1'),
         'CHECKS': ('checks', 'v1alpha'),
         'CHROMEMANAGEMENT': ('chromemanagement', 'v1'),
         'CHROMEPOLICY': ('chromepolicy', 'v1'),
         'CHROMEUXREPORT': ('chromeuxreport', 'v1'),
         'CIVICINFO': ('civicinfo', 'v2'),
         'CLASSROOM': ('classroom', 'v1'),
         'CLOUDASSET': ('cloudasset', 'v1'),
         'CLOUDBILLING': ('cloudbilling', 'v1'),
         'CLOUDBUILD': ('cloudbuild', 'v2'),
         'CLOUDCHANNEL': ('cloudchannel', 'v1'),
         'CLOUDCONTROLSPARTNER': ('cloudcontrolspartner', 'v1'),
         'CLOUDDEPLOY': ('clouddeploy', 'v1'),
         'CLOUDERRORREPORTING': ('clouderrorreporting', 'v1beta1'),
         'CLOUDFUNCTIONS': ('cloudfunctions', 'v2'),
         'CLOUDIDENTITY': ('cloudidentity', 'v1'),
         'CLOUDKMS': ('cloudkms', 'v1'),
         'CLOUDPROFILER': ('cloudprofiler', 'v2'),
         'CLOUDRESOURCEMANAGER': ('cloudresourcemanager', 'v3'),
         'CLOUDSCHEDULER': ('cloudscheduler', 'v1'),
         'CLOUDSEARCH': ('cloudsearch', 'v1'),
         'CLOUDSHELL': ('cloudshell', 'v1'),
         'CLOUDSUPPORT': ('cloudsupport', 'v2'),
         'CLOUDTASKS': ('cloudtasks', 'v2'),
         'CLOUDTRACE': ('cloudtrace', 'v2'),
         'COMPOSER': ('composer', 'v1'),
         'COMPUTE': ('compute', 'v1'),
         'CONFIG': ('config', 'v1'),
         'CONNECTORS': ('connectors', 'v2'),
         'CONTACTCENTERAIPLATFORM': ('contactcenteraiplatform', 'v1alpha1'),
         'CONTACTCENTERINSIGHTS': ('contactcenterinsights', 'v1'),
         'CONTAINER': ('container', 'v1'),
         'CONTAINERANALYSIS': ('containeranalysis', 'v1'),
         'CONTENT': ('content', 'v2.1'),
         'CONTENTWAREHOUSE': ('contentwarehouse', 'v1'),
         'CSS': ('css', 'v1'),
         'CUSTOMSEARCH': ('customsearch', 'v1'),
         'DATACATALOG': ('datacatalog', 'v1'),
         'DATAFLOW': ('dataflow', 'v1b3'),
         'DATAFORM': ('dataform', 'v1beta1'),
         'DATAFUSION': ('datafusion', 'v1'),
         'DATALABELING': ('datalabeling', 'v1beta1'),
         'DATALINEAGE': ('datalineage', 'v1'),
         'DATAMIGRATION': ('datamigration', 'v1'),
         'DATAPIPELINES': ('datapipelines', 'v1'),
         'DATAPLEX': ('dataplex', 'v1'),
         'DATAPORTABILITY': ('dataportability', 'v1'),
         'DATAPROC': ('dataproc', 'v1'),
         'DATASTORE': ('datastore', 'v1'),
         'DATASTREAM': ('datastream', 'v1'),
         'DEPLOYMENTMANAGER': ('deploymentmanager', 'v2'),
         'DEVELOPERCONNECT': ('developerconnect', 'v1'),
         'DFAREPORTING': ('dfareporting', 'v4'),
         'DIALOGFLOW': ('dialogflow', 'v3'),
         'DIGITALASSETLINKS': ('digitalassetlinks', 'v1'),
         'DISCOVERY': ('discovery', 'v1'),
         'DISCOVERYENGINE': ('discoveryengine', 'v1'),
         'DISPLAYVIDEO': ('displayvideo', 'v4'),
         'DLP': ('dlp', 'v2'),
         'DNS': ('dns', 'v1'),
         'DOCS': ('docs', 'v1'),
         'DOCUMENTAI': ('documentai', 'v1'),
         'DOMAINS': ('domains', 'v1'),
         'DOUBLECLICKBIDMANAGER': ('doubleclickbidmanager', 'v2'),
         'DOUBLECLICKSEARCH': ('doubleclicksearch', 'v2'),
         'DRIVE': ('drive', 'v3'),
         'DRIVEACTIVITY': ('driveactivity', 'v2'),
         'DRIVELABELS': ('drivelabels', 'v2'),
         'ESSENTIALCONTACTS': ('essentialcontacts', 'v1'),
         'EVENTARC': ('eventarc', 'v1'),
         'FACTCHECKTOOLS': ('factchecktools', 'v1alpha1'),
         'FCM': ('fcm', 'v1'),
         'FCMDATA': ('fcmdata', 'v1beta1'),
         'FILE': ('file', 'v1'),
         'FIREBASE': ('firebase', 'v1beta1'),
         'FIREBASEAPPCHECK': ('firebaseappcheck', 'v1'),
         'FIREBASEAPPDISTRIBUTION': ('firebaseappdistribution', 'v1'),
         'FIREBASEDATABASE': ('firebasedatabase', 'v1beta'),
         'FIREBASEDATACONNECT': ('firebasedataconnect', 'v1beta'),
         'FIREBASEDYNAMICLINKS': ('firebasedynamiclinks', 'v1'),
         'FIREBASEHOSTING': ('firebasehosting', 'v1'),
         'FIREBASEML': ('firebaseml', 'v1'),
         'FIREBASERULES': ('firebaserules', 'v1'),
         'FIREBASESTORAGE': ('firebasestorage', 'v1beta'),
         'FIRESTORE': ('firestore', 'v1'),
         'FITNESS': ('fitness', 'v1'),
         'FORMS': ('forms', 'v1'),
         'GAMES': ('games', 'v1'),
         'GAMESCONFIGURATION': ('gamesConfiguration', 'v1configuration'),
         'GAMESMANAGEMENT': ('gamesManagement', 'v1management'),
         'GKEBACKUP': ('gkebackup', 'v1'),
         'GKEHUB': ('gkehub', 'v2'),
         'GKEONPREM': ('gkeonprem', 'v1'),
         'GMAIL': ('gmail', 'v1'),
         'GMAILPOSTMASTERTOOLS': ('gmailpostmastertools', 'v1'),
         'GROUPSMIGRATION': ('groupsmigration', 'v1'),
         'GROUPSSETTINGS': ('groupssettings', 'v1'),
         'HEALTHCARE': ('healthcare', 'v1'),
         'HOMEGRAPH': ('homegraph', 'v1'),
         'IAM': ('iam', 'v2'),
         'IAMCREDENTIALS': ('iamcredentials', 'v1'),
         'IAP': ('iap', 'v1'),
         'IDENTITYTOOLKIT': ('identitytoolkit', 'v3'),
         'IDS': ('ids', 'v1'),
         'INDEXING': ('indexing', 'v3'),
         'INTEGRATIONS': ('integrations', 'v1'),
         'JOBS': ('jobs', 'v4'),
         'KEEP': ('keep', 'v1'),
         'KGSEARCH': ('kgsearch', 'v1'),
         'KMSINVENTORY': ('kmsinventory', 'v1'),
         'LANGUAGE': ('language', 'v2'),
         'LIBRARYAGENT': ('libraryagent', 'v1'),
         'LICENSING': ('licensing', 'v1'),
         'LIFESCIENCES': ('lifesciences', 'v2beta'),
         'LOCALSERVICES': ('localservices', 'v1'),
         'LOGGING': ('logging', 'v2'),
         'LOOKER': ('looker', 'v1'),
         'MANAGEDIDENTITIES': ('managedidentities', 'v1'),
         'MANAGEDKAFKA': ('managedkafka', 'v1'),
         'MANUFACTURERS': ('manufacturers', 'v1'),
         'MARKETINGPLATFORMADMIN': ('marketingplatformadmin', 'v1alpha'),
         'MEET': ('meet', 'v2'),
         'MEMCACHE': ('memcache', 'v1'),
         'MERCHANTAPI': ('merchantapi', 'reviews_v1beta'),
         'METASTORE': ('metastore', 'v2'),
         'MIGRATIONCENTER': ('migrationcenter', 'v1'),
         'ML': ('ml', 'v1'),
         'MONITORING': ('monitoring', 'v3'),
         'MYBUSINESSACCOUNTMANAGEMENT': ('mybusinessaccountmanagement', 'v1'),
         'MYBUSINESSBUSINESSINFORMATION': ('mybusinessbusinessinformation', 'v1'),
         'MYBUSINESSLODGING': ('mybusinesslodging', 'v1'),
         'MYBUSINESSNOTIFICATIONS': ('mybusinessnotifications', 'v1'),
         'MYBUSINESSPLACEACTIONS': ('mybusinessplaceactions', 'v1'),
         'MYBUSINESSQANDA': ('mybusinessqanda', 'v1'),
         'MYBUSINESSVERIFICATIONS': ('mybusinessverifications', 'v1'),
         'NETAPP': ('netapp', 'v1'),
         'NETWORKCONNECTIVITY': ('networkconnectivity', 'v1'),
         'NETWORKMANAGEMENT': ('networkmanagement', 'v1'),
         'NETWORKSECURITY': ('networksecurity', 'v1'),
         'NETWORKSERVICES': ('networkservices', 'v1'),
         'NOTEBOOKS': ('notebooks', 'v2'),
         'OAUTH2': ('oauth2', 'v2'),
         'ONDEMANDSCANNING': ('ondemandscanning', 'v1'),
         'ORACLEDATABASE': ('oracledatabase', 'v1'),
         'ORGPOLICY': ('orgpolicy', 'v2'),
         'OSCONFIG': ('osconfig', 'v1'),
         'OSLOGIN': ('oslogin', 'v1'),
         'PAGESPEEDONLINE': ('pagespeedonline', 'v5'),
         'PARALLELSTORE': ('parallelstore', 'v1'),
         'PAYMENTSRESELLERSUBSCRIPTION': ('paymentsresellersubscription', 'v1'),
         'PEOPLE': ('people', 'v1'),
         'PLACES': ('places', 'v1'),
         'PLAYCUSTOMAPP': ('playcustomapp', 'v1'),
         'PLAYDEVELOPERREPORTING': ('playdeveloperreporting', 'v1beta1'),
         'PLAYGROUPING': ('playgrouping', 'v1alpha1'),
         'PLAYINTEGRITY': ('playintegrity', 'v1'),
         'POLICYANALYZER': ('policyanalyzer', 'v1'),
         'POLICYSIMULATOR': ('policysimulator', 'v1'),
         'POLICYTROUBLESHOOTER': ('policytroubleshooter', 'v1'),
         'POLLEN': ('pollen', 'v1'),
         'POLY': ('poly', 'v1'),
         'PRIVATECA': ('privateca', 'v1'),
         'PROD_TT_SASPORTAL': ('prod_tt_sasportal', 'v1alpha1'),
         'PUBLICCA': ('publicca', 'v1'),
         'PUBSUB': ('pubsub', 'v1'),
         'PUBSUBLITE': ('pubsublite', 'v1'),
         'RAPIDMIGRATIONASSESSMENT': ('rapidmigrationassessment', 'v1'),
         'READERREVENUESUBSCRIPTIONLINKING': ('readerrevenuesubscriptionlinking',
                                              'v1'),
         'REALTIMEBIDDING': ('realtimebidding', 'v1'),
         'RECAPTCHAENTERPRISE': ('recaptchaenterprise', 'v1'),
         'RECOMMENDATIONENGINE': ('recommendationengine', 'v1beta1'),
         'RECOMMENDER': ('recommender', 'v1'),
         'REDIS': ('redis', 'v1'),
         'RESELLER': ('reseller', 'v1'),
         'RETAIL': ('retail', 'v2'),
         'RUN': ('run', 'v2'),
         'RUNTIMECONFIG': ('runtimeconfig', 'v1'),
         'SAFEBROWSING': ('safebrowsing', 'v5'),
         'SASPORTAL': ('sasportal', 'v1alpha1'),
         'SCRIPT': ('script', 'v1'),
         'SEARCHADS360': ('searchads360', 'v0'),
         'SEARCHCONSOLE': ('searchconsole', 'v1'),
         'SECRETMANAGER': ('secretmanager', 'v1'),
         'SECURITYCENTER': ('securitycenter', 'v1'),
         'SECURITYPOSTURE': ('securityposture', 'v1'),
         'SERVICECONSUMERMANAGEMENT': ('serviceconsumermanagement', 'v1'),
         'SERVICECONTROL': ('servicecontrol', 'v2'),
         'SERVICEDIRECTORY': ('servicedirectory', 'v1'),
         'SERVICEMANAGEMENT': ('servicemanagement', 'v1'),
         'SERVICENETWORKING': ('servicenetworking', 'v1'),
         'SERVICEUSAGE': ('serviceusage', 'v1'),
         'SHEETS': ('sheets', 'v4'),
         'SITEVERIFICATION': ('siteVerification', 'v1'),
         'SLIDES': ('slides', 'v1'),
         'SMARTDEVICEMANAGEMENT': ('smartdevicemanagement', 'v1'),
         'SOLAR': ('solar', 'v1'),
         'SPANNER': ('spanner', 'v1'),
         'SPEECH': ('speech', 'v1'),
         'SQLADMIN': ('sqladmin', 'v1'),
         'STORAGE': ('storage', 'v1'),
         'STORAGETRANSFER': ('storagetransfer', 'v1'),
         'STREETVIEWPUBLISH': ('streetviewpublish', 'v1'),
         'STS': ('sts', 'v1'),
         'TAGMANAGER': ('tagmanager', 'v2'),
         'TASKS': ('tasks', 'v1'),
         'TESTING': ('testing', 'v1'),
         'TEXTTOSPEECH': ('texttospeech', 'v1'),
         'TOOLRESULTS': ('toolresults', 'v1beta3'),
         'TPU': ('tpu', 'v2'),
         'TRAFFICDIRECTOR': ('trafficdirector', 'v3'),
         'TRANSCODER': ('transcoder', 'v1'),
         'TRANSLATE': ('translate', 'v3'),
         'TRAVELIMPACTMODEL': ('travelimpactmodel', 'v1'),
         'VAULT': ('vault', 'v1'),
         'VERIFIEDACCESS': ('verifiedaccess', 'v2'),
         'VERSIONHISTORY': ('versionhistory', 'v1'),
         'VIDEOINTELLIGENCE': ('videointelligence', 'v1'),
         'VISION': ('vision', 'v1'),
         'VMMIGRATION': ('vmmigration', 'v1'),
         'VMWAREENGINE': ('vmwareengine', 'v1'),
         'VPCACCESS': ('vpcaccess', 'v1'),
         'WALLETOBJECTS': ('walletobjects', 'v1'),
         'WEBFONTS': ('webfonts', 'v1'),
         'WEBRISK': ('webrisk', 'v1'),
         'WEBSECURITYSCANNER': ('websecurityscanner', 'v1'),
         'WORKFLOWEXECUTIONS': ('workflowexecutions', 'v1'),
         'WORKFLOWS': ('workflows', 'v1'),
         'WORKLOADMANAGER': ('workloadmanager', 'v1'),
         'WORKSPACEEVENTS': ('workspaceevents', 'v1'),
         'WORKSTATIONS': ('workstations', 'v1'),
         'YOUTUBE': ('youtube', 'v3'),
         'YOUTUBEANALYTICS': ('youtubeAnalytics', 'v2'),
         'YOUTUBEREPORTING': ('youtubereporting', 'v1')})


Service = S('Service', list(SERVICE_DEFINITIONS.keys()))
