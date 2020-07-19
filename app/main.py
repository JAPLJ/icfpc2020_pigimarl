import sys

sys.path.append("/Users/um003592/icfpc2020/icfpc2020_pigimarl/tools")

import orbit_and_stop
import tournament_client


def main():
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])

    sol1 = orbit_and_stop.OrbitStop()
    sol2 = orbit_and_stop.OrbitStop()

    tournament_client.run(server_url, player_key, sol1, sol2)


if __name__ == '__main__':
    main()
