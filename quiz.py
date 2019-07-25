from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABc9-3vl7axhmpucu0xhOTDMROLu0ihsnHeqph6OSUUFPS27-Y58CkRZY4O1RgjsJwM5caNw6BDCdq3-cGaH1N69k-B126NmnSb9EL9ARyq4oRgslIFSOmBQHHIZOvjjaV-ZzCzojfz0duX9Cs2KjqI5USn8GUjzWXxwhV8zY4hECNAN3c='


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()