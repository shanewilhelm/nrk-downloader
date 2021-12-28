import requests
import bs4
import json
import ffmpeg
import argparse
import re


def main():
    parser = create_parser()
    args = parser.parse_args()
    page_url = args.video_url
    series_name = get_series_name(page_url)

    if args.series > 0:
        download_series(series_name)
    elif args.season > 0:
        season_num = get_season_number(page_url)
        download_season(series_name, season_num)
    else:
        download_video(get_program_id(page_url), series_name)


def create_parser():
    parser = argparse.ArgumentParser(description='Download videos from NRK')
    parser.add_argument('video_url', type=str)
    parser.add_argument('--series', '--serie', action='count', default=0)
    parser.add_argument('--season', '--sesong', action='count', default=0)
    return parser


def get_program_id(page_url):
    page = requests.get(page_url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    program_meta = soup.find("meta", property="nrk:program-id")
    if program_meta is None:
        return None
    program_id = program_meta["content"]
    return program_id


def get_series_name(page_url):
    return re.search('/serie/([^/\\s]+)', page_url).group(1)


def get_season_number(page_url):
    match = re.search('/sesong/([^/\\s]+)', page_url)
    if match is None:
        raise RuntimeError("Failed to find Season number in URL")
    else:
        return match.group(1)


def download_video(program_id, output_name):
    response = requests.get("https://psapi.nrk.no/playback/manifest/program/" + program_id)
    program_data = json.loads(response.text)
    video_url = program_data["playable"]["assets"][0]["url"]
    save_video(video_url, output_name)


def save_video(video_url, output_name):
    (
        ffmpeg
        .input(video_url)
        .output(output_name + '.mp4', c="copy", **{'bsf:a': 'aac_adtstoasc'})
        .run()
    )


def download_season(series_name, season_num):
    episode_num = 1
    while True:
        episode_url = 'https://tv.nrk.no/serie/' + series_name + '/sesong/' + \
                      str(season_num) + '/episode/' + str(episode_num)
        program_id = get_program_id(episode_url)
        if program_id is None:
            return

        download_video(program_id, series_name + '_S' + str(season_num) + '_E' + str(episode_num))
        episode_num += 1


def season_exists(series_name, season_num):
    response = requests.get('https://tv.nrk.no/serie/' + series_name + '/sesong/' + str(season_num))
    if len(response.history) == 0:
        # No redirects
        return True
    else:
        return False


def download_series(series_name):
    season_num = 1
    while True:
        if not season_exists(series_name, season_num):
            return
        download_season(series_name, season_num)
        season_num += 1


if __name__ == "__main__":
    main()
