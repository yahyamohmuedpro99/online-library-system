import random
from datetime import datetime, date, timedelta
from faker import Faker

fake = Faker()

class MockDataGenerator:
    """Generate realistic mock data for the library system"""
    
    BOOK_CATEGORIES = [
        'Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 
        'Romance', 'Thriller', 'Biography', 'History', 'Science', 
        'Technology', 'Self-Help', 'Business', 'Health', 'Travel',
        'Cooking', 'Art', 'Philosophy', 'Religion', 'Poetry'
    ]
    
    FAMOUS_AUTHORS = [
        'Stephen King', 'J.K. Rowling', 'George R.R. Martin', 'Agatha Christie',
        'Dan Brown', 'John Grisham', 'Margaret Atwood', 'Neil Gaiman',
        'Haruki Murakami', 'Toni Morrison', 'Ernest Hemingway', 'Jane Austen',
        'Mark Twain', 'Charles Dickens', 'Virginia Woolf', 'F. Scott Fitzgerald',
        'Gabriel García Márquez', 'Maya Angelou', 'Paulo Coelho', 'Yuval Noah Harari'
    ]
    
    @staticmethod
    def generate_book_data(count=50):
        """Generate mock book data"""
        books = []
        
        for _ in range(count):
            # Generate release date between 1950 and 2024
            start_date = date(1950, 1, 1)
            end_date = date(2024, 12, 31)
            time_between = end_date - start_date
            days_between = time_between.days
            random_days = random.randrange(days_between)
            release_date = start_date + timedelta(days=random_days)
            
            book = {
                'title': fake.catch_phrase() + ': ' + fake.bs().title(),
                'author': random.choice(MockDataGenerator.FAMOUS_AUTHORS),
                'category': random.choice(MockDataGenerator.BOOK_CATEGORIES),
                'price': round(random.uniform(9.99, 99.99), 2),
                'release_date': release_date.strftime('%Y-%m-%d'),
                'description': fake.text(max_nb_chars=500)
            }
            books.append(book)
        
        return books
    
    @staticmethod
    def generate_user_data(count=20):
        """Generate mock user data"""
        users = []
        
        for _ in range(count):
            user = {
                'email': fake.unique.email(),
                'password': 'password123'  # Simple password for testing
            }
            users.append(user)
        
        return users
    
    @staticmethod
    def generate_specific_books():
        """Generate some specific well-known books for better testing"""
        specific_books = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'category': 'Fiction',
                'price': 12.99,
                'release_date': '1925-04-10',
                'description': 'A classic American novel set in the Jazz Age, exploring themes of wealth, love, and the American Dream.'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'category': 'Fiction',
                'price': 14.99,
                'release_date': '1960-07-11',
                'description': 'A gripping tale of racial injustice and childhood innocence in the American South.'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'category': 'Science Fiction',
                'price': 13.99,
                'release_date': '1949-06-08',
                'description': 'A dystopian social science fiction novel about totalitarian control and surveillance.'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'category': 'Romance',
                'price': 11.99,
                'release_date': '1813-01-28',
                'description': 'A romantic novel that critiques the British landed gentry at the end of the 18th century.'
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'category': 'Fiction',
                'price': 13.50,
                'release_date': '1951-07-16',
                'description': 'A controversial novel about teenage rebellion and alienation in post-war America.'
            },
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'author': 'J.K. Rowling',
                'category': 'Fantasy',
                'price': 15.99,
                'release_date': '1997-06-26',
                'description': 'The first book in the beloved Harry Potter series about a young wizard\'s adventures.'
            },
            {
                'title': 'The Lord of the Rings',
                'author': 'J.R.R. Tolkien',
                'category': 'Fantasy',
                'price': 25.99,
                'release_date': '1954-07-29',
                'description': 'An epic high fantasy novel about the quest to destroy the One Ring.'
            },
            {
                'title': 'Sapiens: A Brief History of Humankind',
                'author': 'Yuval Noah Harari',
                'category': 'History',
                'price': 18.99,
                'release_date': '2011-01-01',
                'description': 'A thought-provoking exploration of human history and our species\' impact on the world.'
            },
            {
                'title': 'The Da Vinci Code',
                'author': 'Dan Brown',
                'category': 'Thriller',
                'price': 16.99,
                'release_date': '2003-03-18',
                'description': 'A mystery thriller that follows symbologist Robert Langdon as he investigates a murder.'
            },
            {
                'title': 'Steve Jobs',
                'author': 'Walter Isaacson',
                'category': 'Biography',
                'price': 19.99,
                'release_date': '2011-10-24',
                'description': 'The definitive biography of Apple co-founder Steve Jobs, based on exclusive interviews.'
            }
        ]
        
        return specific_books
