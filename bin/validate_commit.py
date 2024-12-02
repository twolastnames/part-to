#!/usr/bin/env python3
import shared as shared
import sys

def validate_message(message):
    for semanticPrefix in shared.semanticPrefixes:
        try:
            semanticPrefix.validate_commit_message(message)
        except shared.SemanticPrefixUnknown:
            continue
        return
    raise shared.SemanticPrefixUnknown()

def notify_message_validation_error():
    print('\n'.join([
        'The commit prefix was invalid/unknown. A commit message should start',
        'with a known prefix followed directly by a colon, Please use one of ',
        'the following prefixes for the described purposes:',
    ]))
    for semanticPrefix in shared.semanticPrefixes:
        print(semanticPrefix)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('filename with commit needed is input')
        exit(1)
    file = open(sys.argv[1])
    text = file.read()
    file.close()
    try:
        validate_message(text)
    except shared.SemanticPrefixUnknown:
        notify_message_validation_error()
        exit(1)
    print("Passed Commit Semantics")
    exit(0)

