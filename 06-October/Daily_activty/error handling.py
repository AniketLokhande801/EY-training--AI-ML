while True:
    try:
        a=int(input("enter number"))
        print(10/a)
    except ZeroDivisionError:
        print("division by zero")
    except ValueError:
        print("value must be an integer")
    finally:
        print("excuted")