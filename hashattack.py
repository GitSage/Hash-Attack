import hashlib
import argparse
import random
import string
import time

def rand_word():
    length = random.randint(6, 25)
    return ''.join(random.choice(string.digits + string.ascii_letters + '!@#$%^&* ') for _ in range(length))

sha = hashlib.sha1

print "SAGE HASH ATTACK"

# parse arguments
parser = argparse.ArgumentParser(description='This program will attempt perform a collision or preimage attack.')
parser.add_argument('--attack', '-a', help='The kind of attack to perform (collision or preimage)',
                    default='collision', choices=['collision', 'preimage'], action='store')
parser.add_argument('--num-repetitions', '-r', help='The number of repetitions to perform.',
                    type=int, default=20, action='store')
parser.add_argument('--num-bits', '-b', help='The size of the hash in bits.', type=int, default=20,
                    choices=xrange(4, 128, 4), action='store')
parser.add_argument('--message', '-m', help='Message to be matched in a preimage attack', default=rand_word())
args = parser.parse_args()

attack_type = args.attack
reps = args.num_repetitions
num_bits = args.num_bits
message = args.message

# perform a collision attack
if attack_type == 'collision':
    total_time = 0
    total_failures = 0
    print "Running %d collision tests with %d bits" % (reps, num_bits)
    print "Test # |   Failures | Time Spent | Strings"
    print "---------------------------------------------------"
    for i in range(reps):
        start_time = time.time()
        failures = 0
        hashes = {}
        while True:
            # generate random random word
            word = rand_word()

            # hash and truncate the word
            my_hash = sha(word).hexdigest()[0:num_bits/4]

            # check if this is a collision
            if my_hash in hashes:
                time_spent = time.time() - start_time
                total_failures += len(hashes)
                total_time += time_spent
                print "%6d | %10d | %9fs | %s, %s" % (i+1, len(hashes), time_spent, word, hashes[my_hash])
                break

            hashes[my_hash] = word

    print "%6s | %10d | %9fs |" % ("Total", total_failures, total_time)
    print "%6s | %10d | %9fs |" % ("Avg", total_failures/reps, total_time/reps)

# perform a preimage attack
elif attack_type == 'preimage':
    total_failures = 0
    total_time = 0
    print "Running %d preimage attacks with %d bits and message '%s'" % (reps, num_bits, message)
    message_hash = sha(message).hexdigest()[0:num_bits/4]
    print "Your message hashes to %s" % message_hash
    print "Test # |   Failures | Time Spent | Collision String"
    print "---------------------------------------------------"
    for i in range(reps):
        start_time = time.time()
        failures = 0
        while True:
            word = rand_word()
            # hash and truncate a random word
            my_hash = sha(word).hexdigest()[0:num_bits/4]

            # check if the hash matches
            if my_hash == message_hash:
                time_spent = time.time() - start_time
                total_failures += failures
                total_time += time_spent
                print "%6d | %10d | %9fs | %s" % (i+1, failures, time_spent, word)
                break
            failures += 1
    print "%6s | %10d | %9fs | %s" % ("Total", total_failures, total_time, "")
    print "%6s | %10d | %9fs | %s" % ("Avg", total_failures/reps, total_time/reps, "")
