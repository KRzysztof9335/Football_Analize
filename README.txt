Application structure

Modules:
    - infobank (ib)
    - parser_html (ph)

Sources:
    - wf - worldfootball.net
    - fd - footballdata.uk

Variable names suffixes:
    - A - array
    - AA - array of arrays
    - AD - array of dictionaries
    - S - string
    - I - integer number
    - F - float number
    - C - class
    - B - bolean

Main.py
    Database"
        Germany:
            bundesliga
                2017-2018
                    Round1
                        round_table.txt
                        match__team1_team2.txt
                        match__team3_team4.txt
                    Round2
                        ...
                    Round3

Legend:H-Home A-Away

match__team1_team2.txt
(world football)
    match_date
    match_hour
    match_home_team(team1)
    match_away_team(team1)
    HTFT(FullTime)
    ATFT
    HTHT(HalfTime)
    ATHT
    match_report

(football data)
    HS(shots)
    AS
    HST(shotsontarget)
    AST
    HC(corners)
    AC
    HY(yellowcards)
    AY
    HR(redcards)
    AR
    B365H(bet365homewins)
    B365D(bet365draw)
    B365A(bet365awaywins)
Placeforadditionalinfo...
ForGermanyconsiderPlayerNotes


round_table.txt
place;team1;matches_played;matches_won;matches_draw;matches_lost;goals_shot:goals_lost;goals_diff;points
place;team2;matches_played;matches_won;matches_draw;matches_lost;goals_shot:goals_lost;goals_diff;points
...
