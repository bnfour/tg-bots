<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
        <title>telegram bot(s) index</title>
        <style type="text/css">
            html {
                width: 100%;
            }
            
            body {
                /* centers the wrapper horizontally */
                display: flex;
                flex-direction: row;
                justify-content: center;

                font-family: 'Noto Sans', 'Droid Sans', Helvetica, Arial, sans-serif;
            }

            .wrapper {
                display: flex;
                flex-direction: column;
            }

            h1, h2 {
                font-family: 'Iosevka', 'Consolas', 'Courier New', Courier, monospace;
            }

            .bot-list > *:not(:last-child)::after {
                content: " · ";
            }

            @media (prefers-color-scheme: dark) {
                body {
                    color: #ccc;
                    background-color: #333;
                }

                a:link {
                    color: #a0a0ff;
                }

                a:visited {
                    color: #f0a0f0;
                }

                a:active {
                    color: #fff;
                }

                img.bw {
                    filter: invert(0.8);
                }
            }
        </style>
    </head>
    <body>
        <div class="wrapper">
            <h1>human presence is discouraged</h1>
            <h2>щитпостинг ботс галоре</h2>
            <p>This site hosts bnfour's telegram bots. See more info on that on <a href="https://github.com/bnfour/tg-bots">GitHub repo</a>.</p>
            % include('bot_list.tpl', data=data)
        </div>
    </body>
</html>
