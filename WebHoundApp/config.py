from datetime import datetime

msgs = {
    'trace_not_done': 'Your trace is still not complete. Your hound should be back soon, either reload this page or type the same name in the homepage to check again.',
}

errors = {
    'no_trace_name': 'No trace name supplied',
    'no_name_in_db': 'The supplied trace name is not in the database',
    'no_task_ts': 'The task has no (default) timestamp',
    'unknown_sherlock': 'Unexpected branch for sherlock task logic',
}

cfg_data = {
    'default_task_ts': datetime.strptime('01.01.1990+0000', '%d.%m.%Y%z'),
    'sherlock_results_dir': "WebHoundApp/sherlock/results/{}.csv",
    'sherlock_unix_cmd': "python WebHoundApp/sherlock/sherlock -o WebHoundApp/sherlock/results/{trace_name}.csv --csv --print-found {trace_name}",
    'sherlock_win_cmd': "python WebHoundApp\\sherlock\\sherlock -o WebHoundApp\\sherlock\\results\\{trace_name}.csv --csv --print-found {trace_name}",
}

cfg_test = {
    'put_data': "https://500px.com/meggamorty ; https://www.cnet.com/profiles/meggamorty/ ; https://www.chess.com/ru/member/meggamorty ; https://www.discogs.com/user/meggamorty ; https://disqus.com/meggamorty ; https://www.ebay.com/usr/meggamorty ; https://euw.op.gg/summoner/userName=meggamorty ; https://flipboard.com/@meggamorty ; https://fortnitetracker.com/profile/all/meggamorty ; https://www.freelancer.com/api/users/0.1/users?usernames%5B%5D=meggamorty&compact=true ; https://www.instagram.com/meggamorty ; https://meggamorty.itch.io/ ; https://www.kaggle.com/meggamorty ; https://leetcode.com/meggamorty ; https://photobucket.com/user/meggamorty/library ; https://rateyourmusic.com/~meggamorty ; https://www.redbubble.com/people/meggamorty ; https://www.reddit.com/user/meggamorty ; https://open.spotify.com/user/meggamorty ; https://steamcommunity.com/id/meggamorty ; https://steamid.uk/profile/meggamorty ; https://www.gotinder.com/@meggamorty ; https://www.twitter.com/meggamorty ; https://ultimate-guitar.com/u/meggamorty ; https://www.wikipedia.org/wiki/User:meggamorty ; https://www.youtube.com/meggamorty ; https://tracr.co/users/1/meggamorty ; Total Websites Username Detected On : 27 ; ",
}