updatemenus=list([
    dict(
        buttons=list([   
            dict(
                args=['nativeEnglish', True],
                label='Selected',
                method='restyle'
            ),
            dict(
                args=['nativeEnglish', False],
                label='Not Selected',
                method='restyle'
            ),                    
        ]),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.775,
        xanchor = 'left',
        y = 0.5,
        yanchor = 'top'            
    ),
   dict(
        buttons=list([   
            dict(
                args=['analyticMajor', True],
                label='Selected',
                method='restyle'
            ),
            dict(
                args=['analyticMajor', False],
                label='Not Selected',
                method='restyle'
            ),                    
        ]),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.775,
        xanchor = 'left',
        y = 0.5,
        yanchor = 'top'            
    ),
])

annotations = list([
    dict(text='Native<br>English', x=0, y=1.11, yref='paper', align='left', showarrow=False ),
    dict(text='Analytic<br>Major', x=0.25, y=1.11, yref='paper', showarrow=False ),
])
layout['updatemenus'] = updatemenus
layout['annotations'] = annotations
