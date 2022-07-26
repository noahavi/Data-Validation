import faker
import pytz
import random
from collections import Counter
from datetime import datetime


# Generate random date in iso format
def iso_date():
    fake = faker.Faker()
    rand_date = fake.date_time()
    rand_date_iso = rand_date.isoformat()
    return rand_date_iso


# Generate random date in non iso format
def reg_date():
    fake = faker.Faker()
    return fake.date_time()


def random_text():
    fake = faker.Faker()
    return fake.text(random.randrange(5, 30))


# Generate random timezone to append to dates
def random_tz():
    randZoneName = random.choice(pytz.all_timezones)  # Random timezone
    randZone = datetime.now(pytz.timezone(randZoneName))  # Get date at timezone
    offset = randZone.strftime("%z")  # Slice off timezone
    if str(offset[1:3]) == "00" and str(offset[3:]) == "00":  # Change '00:00' to Z
        return "Z"
    return str(offset[:3] + ":" + offset[3:])


def generate_dataset(size):
    dataset_name = "data.txt"
    dataset_test_name = "data_test.txt"
    duplicate_range = 3  # range of possible duplicates for date
    date_type_thresh = 0.5  # adjust ratio of iso format to non iso format
    with open(dataset_name, "w", newline="") as txtfile, open(
        dataset_test_name, "w", newline=""
    ) as txtfile_test:
        seed = 0
        for _ in range(size):
            seed += 1
            # Random val above threshold -> write iso format date
            # Random val below threshold -> write non iso format date
            if random.random() >= date_type_thresh:
                date = iso_date()
                tz = random_tz()
                # Always write correct format to test, no duplicates
                txtfile_test.write(str(date) + str(tz) + "\n")
                # Randomly write duplicates to dataset
                for _ in range(random.randrange(1, duplicate_range)):
                    txtfile.write(str(date) + str(tz) + "\n")
            elif random.random() > (date_type_thresh / 2):
                # Non iso format dates
                tz = random_tz()
                date = reg_date()
                for _ in range(random.randrange(1, duplicate_range)):
                    txtfile.write(str(date) + str(tz) + "\n")
            else:  # Random text
                text = random_text()
                for _ in range(random.randrange(1, duplicate_range)):
                    txtfile.write(str(text) + "\n")
    return dataset_name, dataset_test_name


def test_uniques(data, test_data):
    with open(data, "r", newline="") as dataset, open(
        test_data, "r", newline=""
    ) as test_dataset:
        # Each date is added to set if valid format
        # Set holds only unique values
        dataset = set(line.strip() for line in dataset if check_format(line.strip()))
        # Test holds all the dates that must be validated
        test = list(line.strip() for line in test_dataset)
        valid = []
        # Any date that is in both test and set1 should be valid and unique
        for date in test:
            if date in dataset:
                valid.append(date)  # List of valid and unique dates
        # Checks if each list contains the same values as the other
        # If test contains all elements from valid, then all elements of test are valid and unique dates
        if Counter(valid) == Counter(test):
            return True
        else:
            return False


def check_format2(date):
    # First check for "T", colons and hypens to be in correct indices
    if date[10:11] != "T":
        return False
    if date[4:5] != "-" and date[7:8] != "-":
        return False
    if date[13:14] != ":" and date[16:17] != ":":
        return False
    if (
        not date[0:4].isdigit()  # First 4 digits for year
        or not date[5:7].isdigit()
        and int(date[5:7]) in range(1, 13)  # Month in range 1-12
        or not date[8:10].isdigit()
        and int(date[8:10]) in range(1, 32)  # Day in range 1 - 31
        or not date[11:13].isdigit()
        and int(date[11:13]) in range(0, 25)  # Hours in range 0-24
        or not date[14:16].isdigit()
        and int(date[14:16]) in range(0, 61)  # Minutes in range 0-60
        or not date[17:19].isdigit()
        and int(date[17:19]) in range(0, 61)  # Seconds in range 0-60
    ):
        print(date)
        return False
    # Timezone
    if date[19:20] == "+" or date[19:20] == "-":
        if not date[20:22].isdigit() and not int(date[20:22]) in range(
            0, 15
        ):  # Timezone in range 0-14
            print(date)
            return False
        if date[22:23] != ":":
            print(date)
            return False
        if (
            # Timezone minutes can only be 00,45,30
            int(date[23:25]) != 00
            and int(date[23:25]) != 45
            and int(date[23:25]) != 30
            and int(date[23:25]) != 60
        ):
            return False
    if date[19:20] == "Z" and len(date) == 20:  # Z valid at end of string
        return True

    return True


def check_format(date):
    # Attempts to put string into datetime object in iso format
    try:
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        return True
    # String is not in iso format
    except:
        print(f"{date} is an invalid format")
        return False


def validation(dataset, test):
    if test_uniques(dataset, test):
        print("Dataset is valid")
    else:
        print("Dataset is invalid")


def main():
    # Size of generated dataset as arg
    dataset, test = generate_dataset(
        10000
    )  # Returns file names for dataset and test dataset
    validation(dataset, test)
    # validation("data.txt", "data_test.txt")


if __name__ == "__main__":
    main()
