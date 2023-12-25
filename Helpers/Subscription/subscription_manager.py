import uuid
import json

# Define the path to the cache file
cache_file_path = 'subscription_cache.json'

async def handle_all_messages(update, context):
        chat_id = str(update.message.chat_id)
        username = update.message.from_user.username
        SubscriptionManager.subscribe_user(chat_id, username)
    


class SubscriptionManager:
    @staticmethod
    def save_subscription_data(button_data):
        # Generate a unique subscription_id
        subscription_id = str(uuid.uuid4())
        
        # Load the existing cache from the file
        try:
            with open(cache_file_path, 'r') as cache_file:
                local_cache = json.load(cache_file)
        except FileNotFoundError:
            local_cache = {}

        # Save button_data to the local_cache using subscription_id as the key
        local_cache[subscription_id] = button_data
        
        # Write the updated cache back to the file
        with open(cache_file_path, 'w') as cache_file:
            json.dump(local_cache, cache_file)

        # Return the subscription_id for use in callback_data
        return subscription_id

    @staticmethod
    def load_subscription_data(subscription_id):
        # Load the existing cache from the file
        try:
            with open(cache_file_path, 'r') as cache_file:
                local_cache = json.load(cache_file)
        except FileNotFoundError:
            return None

        subscription_data = local_cache.get(subscription_id)

        # If the subscription id was found, delete it from local cache
        if subscription_id in local_cache:
            del local_cache[subscription_id]
            # Write the updated cache back to the file
            with open(cache_file_path, 'w') as cache_file:
                json.dump(local_cache, cache_file, indent=4)

        # Return the subscription data
        return subscription_data
    
    @staticmethod
    def subscribe_user(chat_id, username):
        # Load or initialize the subscription data
        try:
            with open(cache_file_path, 'r') as cache_file:
                subscriptions = json.load(cache_file)
        except FileNotFoundError:
            subscriptions = {}

        # Initialize the user if they don't exist in the subscription
        if chat_id not in subscriptions:
            subscriptions[chat_id] = {
                'username': username,
                'sources': {}
            }

        # Write the updated subscription data back to the file
        with open(cache_file_path, 'w') as cache_file:
            json.dump(subscriptions, cache_file, indent=4)

    @staticmethod
    def add_title(chat_id, source, title, last_chapter):
        # Assuming the user has been added by subscribe_user beforehand
        
        # Load the existing subscription data from the file
        with open(cache_file_path, 'r') as cache_file:
            subscriptions = json.load(cache_file)
        
        # Initialize the source if it does not exist for the user
        if source not in subscriptions[chat_id]['sources']:
            subscriptions[chat_id]['sources'][source] = []
            
        titles_and_chapters = subscriptions[chat_id]['sources'][source]
        
        # Check if the title already exists within the source
        for item in titles_and_chapters:
            if item['title'] == title:
                # Fail: Title already present
                return "subscribe:1"

        # Since the title wasn't found, add it along with the last chapter
        titles_and_chapters.append({
            'title': title,
            'last_chapter': last_chapter
        })

        # Write the updated subscription data back to the file
        with open(cache_file_path, 'w') as cache_file:
            json.dump(subscriptions, cache_file, indent=4)
        
        # Success: Title added
        return "subscribe:0"

    

