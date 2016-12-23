from pymongo import MongoClient
import sys, os, datetime, logging, yaml
from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Constants():
    DATE_FORMAT='%a, %d %b %Y %H:%M:%S'
    DATE_FOLDER_FORMAT='%Y%m%d'
    DATE_LOGFILE_FORMAT="%Y%m%d-%H%M%S"
    DB_CORE="core"
    COLLECTION_ACTIVITIES="activities"
    COLLECTION_USER_PROFILES='UserProfiles'
    SHARING_LEVEL_TEAM='team'
    SHARING_LEVEL_ME='me'   
    CONTENT_TYPE='ContentType'
    NOTE='Note'
    COMMENT='Comment'
    MODIFIED_DATE='ModifiedDate'
    TITLE='Title'
    CONTENT='Content'
    CONTENT_SIZE='ContentSize'
    AUTHOR_ID='AuthorId'
    AUTHOR_NAME='AuthorName'
    CREATED_DATE='CreatedDate'
    SHARING_LEVEL='SharingLevel'
    TEAM_ID='TeamId'
    MODIFIED_BY_ID='ModifiedById'
    MODIFIED_BY_NAME='ModifiedByName'
    _ID='_id'
    USER_ID='UserId'
    USER_EMAIL='UserEmail'
    CONTENT_IDENTIFIER='Content-Identifier'
    SUBJECT='Subject'
    FROM='From'
    TO='To'
    DATE='Date'
    SUMMARY='Summary'
    HTML='html'
    FILE_SUFFIX='.eml'

def get_date_filter(num_days):
    dt=datetime.datetime.now()-datetime.timedelta(days=num_days) # contains date time
    ret=datetime.datetime(dt.year,dt.month,dt.day) # only date
    return ret

def check_make_dir(dir_path):
    if os.path.exists(dir_path):
        pass
    else:
        os.mkdir(dir_path)
    return 0

def get_activity_summary(activity):
    return '{}:{},\
            {}:{},\
            {}:{},\
            {}:{},\
            {}:{},\
            {}:{},\
            {}:{},\
            {}:{},\
            {}:{}'\
            .format(Constants.CONTENT_TYPE,activity[Constants.CONTENT_TYPE],\
            Constants.CREATED_DATE,activity[Constants.CREATED_DATE],\
            Constants.AUTHOR_ID,activity[Constants.AUTHOR_ID],\
            Constants.AUTHOR_NAME,activity[Constants.AUTHOR_NAME],\
            Constants.MODIFIED_DATE,activity[Constants.MODIFIED_DATE],\
            Constants.MODIFIED_BY_ID,activity[Constants.MODIFIED_BY_ID],\
            Constants.MODIFIED_BY_NAME,activity[Constants.MODIFIED_BY_NAME],\
            Constants.SHARING_LEVEL,activity[Constants.SHARING_LEVEL],\
            Constants.TEAM_ID,activity[Constants.TEAM_ID])

try:
    config_yaml=yaml.load(open('U:\\GitHubHome\\python\\mongo_project\\mongo_app.yaml','rb').read())

    logtime=datetime.datetime.today().strftime(Constants.DATE_LOGFILE_FORMAT)
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logFilename=config_yaml['log_file_path']+"mi_core_"+logtime+".log"
    logHandler=logging.FileHandler(logFilename)
    logHandler.setLevel(logging.DEBUG)
    logFormat=logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logHandler.setFormatter(logFormat)
    logger.addHandler(logHandler)
    
    logger.info("machine intelligence - core - data extract started...")
       
    modified_date_filter=get_date_filter(int(config_yaml['date_delta']))
    logger.info('modified_date_filter: {}'.format(modified_date_filter))

    client_core=MongoClient(config_yaml['conn_uri'])   
    db_core=client_core.get_database(Constants.DB_CORE)    
    collection_activities=db_core.get_collection(Constants.COLLECTION_ACTIVITIES)
    collection_user_profiles=db_core.get_collection(Constants.COLLECTION_USER_PROFILES)

    query_activities=collection_activities.find({"$or":[{Constants.CONTENT_TYPE:Constants.NOTE},{Constants.CONTENT_TYPE:Constants.COMMENT}], \
                                                 Constants.MODIFIED_DATE:{"$gte":modified_date_filter}},{Constants.CONTENT_TYPE:1,Constants.TITLE:1, \
                                                 Constants.CONTENT:1, Constants.CONTENT_SIZE:1,Constants.AUTHOR_ID:1,Constants.AUTHOR_NAME:1,\
                                                 Constants.CREATED_DATE:1,Constants.MODIFIED_DATE:1,Constants.SHARING_LEVEL:1,Constants.TEAM_ID:1,\
                                                 Constants.MODIFIED_BY_ID:1,Constants.MODIFIED_BY_NAME:1})
    logger.info('query_activities count: {}'.format(query_activities.count()))
          
    for counter, activity in enumerate(query_activities):            
        q_from=collection_user_profiles.find_one({Constants.USER_ID:activity[Constants.MODIFIED_BY_ID]})
        if activity[Constants.SHARING_LEVEL]==Constants.SHARING_LEVEL_TEAM:
            q_to=collection_user_profiles.find({Constants.TEAM_ID:activity[Constants.TEAM_ID]})
            str_to=''
            for counter, elem in enumerate(q_to):
                if counter==0:
                    str_to=elem[Constants.USER_EMAIL]
                else:
                    str_to=';'.join([str_to,elem[Constants.USER_EMAIL]])        
        if activity[Constants.SHARING_LEVEL]==Constants.SHARING_LEVEL_ME:
            str_to=q_from[Constants.USER_EMAIL]

        html_data=activity[Constants.CONTENT]        
        msg = MIMEMultipart()
        msg[Constants.CONTENT_IDENTIFIER]=activity[Constants.CONTENT_TYPE]
        msg[Constants.SUMMARY]=get_activity_summary(activity)
        msg[Constants.SUBJECT] = activity[Constants.TITLE]
        msg[Constants.FROM] = q_from[Constants.USER_EMAIL]
        msg[Constants.TO] = str_to
        msg[Constants.DATE] = activity[Constants.MODIFIED_DATE].strftime(Constants.DATE_FORMAT)
        part = MIMEText(html_data, Constants.HTML)
        msg.attach(part)    
        
        dir_path=os.path.join(config_yaml['eml_file_path'],modified_date_filter.strftime(Constants.DATE_FOLDER_FORMAT))
        check_make_dir(dir_path)

        outfile_name = os.path.join(dir_path, str(activity[Constants._ID])+Constants.FILE_SUFFIX)
        with open(outfile_name, 'w') as outfile:
            gen = generator.Generator(outfile)
            gen.flatten(msg)    

except:
    print('Exception: {}'.format(sys.exc_info()[0]))
    logger.error('Stack Trace: {}'.format(sys.exc_info()))
finally:
    logHandler.close()
    logging.shutdown()
