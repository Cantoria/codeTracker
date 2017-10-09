import requests
import json
import Get_Info.get_info_git as gt
import time

def request_api(api):
    app_key = '&key=ZEaUTt2btGSROV8q3NeOQg(('
    info = requests.get(api + app_key)
    info = info.json()
    return info

def get_syn(git_info):
    tags_list = []
    for item in git_info:
        language = (item["github_language"] if not item["github_language"] == "null" else [])
        tags = (item["github_tags"] if not item["github_tags"] == "null" else [])
        print(language)
        print(tags)
        tags_list.extend(language)
        tags_list.extend(tags)

    print("Tags before: {}".format(tags_list))
    tags_list = gt.delete_duplicate(tags_list)
    # The tags containing "#" should be removed or the query of api will be failed
    remove_list = []
    for item in tags_list:
        if "#" in item:
            remove_list.append(item)
            tags_list.remove(item)
    print("Remove list: {}".format(remove_list))
    print("Tags: {}".format(tags_list))

    syn_list = {}
    for tag in tags_list:
        syn_tags = []
        api = 'https://api.stackexchange.com/2.2/tags/{}/synonyms' \
              '?pagesize=100&order=desc&sort=creation&site=stackoverflow'.format(tag)
        syn_info = request_api(api)
        print("Finding tag {}: {}".format(tag,syn_info))
        syn_info = syn_info["items"]
        if not syn_info == []:
            for item in syn_info:
                syn_tags.append(item["from_tag"])
            syn_list[tag] = syn_tags
            print("The synonymous tags of tag {} are {}".format(tag,syn_tags))
        else:
            print("The synonymous tags of tag {} not found".format(tag))

    return syn_list


if __name__ == '__main__':
    info_file = '/home/ace/zsj/Get_Info/Info/awesome_test.json'
    f = open(info_file, encoding='utf-8')
    git_info = json.load(f)

    print("Getting the Stack Overflow synonymous tags of github tags...")
    cTime = time.time()
    syn_list = get_syn(git_info)
    print(time.time() - cTime)

    print("Dumping the syn_list...")
    cTime = time.time()
    file = '/home/ace/zsj/Get_Info/Info/syn_list.json'
    with open(file, 'w') as ctfile:
        json.dump(syn_list, ctfile, indent=3)
    print(time.time() - cTime)