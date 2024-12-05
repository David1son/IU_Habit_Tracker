from counter import Counter
from database import get_db, add_counter, increment_counter, get_counter_data
import os
import time
from analyse import calculate_count

#to execute test, type "test_project.py ." in console

class TestCounter:

    def setup_method(self): # naming convention for pytest. everything in bewtween setup and teardown is run
        self.db = get_db("test.db")

        add_counter(self.db,"test_counter","test_description")
        increment_counter(self.db,"test_counter","2024-11-14")
        increment_counter(self.db, "test_counter", "2024-11-15")
        increment_counter(self.db, "test_counter", "2024-11-17")
        increment_counter(self.db, "test_counter", "2024-11-18")


    def test_counter(self): # naming convention: test_blabla
        counter = Counter("test_counter_1","test_description_1")
        counter.store(self.db)

        counter.increment()
        counter.add_event(self.db)
        counter.reset()
        counter.increment()

    def test_db_counter(self):
        data = get_counter_data(self.db,"test_counter")
        assert len(data) == 4

        count = calculate_count(self.db,"test_counter")
        assert count == 4



    def teardown_method(self):
        self.db.close()
        os.remove("test.db")

# pytest . to run
#testcomment