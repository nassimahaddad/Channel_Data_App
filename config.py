# config_likes.py

# اسم ملف قاعدة البيانات لتطبيق الإعجابات والتفاعلات (applikes.py)
DATABASE_FILE = 'likes_interactions.db'

# دليل لقطات الشاشة/السجلات من برنامج التفاعل التلقائي (auto_interactor.py)
SCREENSHOT_DIR_INTERACTOR = 'selenium_errors_interactor'

# هذا هو معرف المستخدم الثابت لبرنامج auto_interactor.py
# هذا المعرف سيمثل "النظام" الذي يقوم بالإعجابات التلقائية.
# تأكد من أن هذا المعرف فريد ولا يتطابق مع أي معرف مستخدم بشري.
FIXED_INTERACTOR_USER_ID = "auto_interactor_system_id_001"

# --- إعدادات جديدة لتطبيق جمع بيانات القنوات ---
CHANNEL_DATA_DATABASE_FILE = 'channels_data.db' # اسم ملف قاعدة البيانات لتطبيق جمع القنوات

# تأكد من وجود دليل لقطات الشاشة
import os
if not os.path.exists(SCREENSHOT_DIR_INTERACTOR):
    os.makedirs(SCREENSHOT_DIR_INTERACTOR)
