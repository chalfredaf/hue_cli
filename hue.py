

import click
import colorama
import requests
import json



#******************************************************************************
# CLI entry-point
#******************************************************************************
@click.group(invoke_without_command=True, chain=True)
@click.option('-host', default='localhost', help='Bridge IP')
@click.option('-p', default='80', help='Bridge Port')
@click.option('-u', default='localhost', help='HUE user id')
@click.pass_context
def cli(ctx, host, p, u):
    adress = "http://" + host + ':' + p + '/api/' + u
    ctx.ensure_object(dict)
    ctx.obj['ADRESS'] = adress


#******************************************************************************
@cli.command()
@click.option('-f/-nof','--flip', default=False)
def switch(flip):
    click.echo('flipper is: ' + str(flip))
    
    
#******************************************************************************    
@cli.command()
@click.option('-i','--info', is_flag=True)
def test(info):
    if info:
        click.echo('fart!')
    else:
        click.echo('bronk!')


#******************************************************************************
@cli.command()
@click.pass_context
def dist(ctx):
     ctx.forward(test)
     ctx.invoke(test, info=True)

    
#******************************************************************************
@cli.command()
@click.option('-id', required=True, help='light id', type=int)
@click.option('-on', '--enabled', default=True, help='Set on/off')
@click.option('-bri', 
              default=250, 
              help='Set brightness [0...254]', 
              type=click.IntRange(0,254,clamp=True))
@click.option('-hue', 
              required=True, 
              help="Set Hue", 
              type=click.Choice(['blue','green','yellow','red']))
@click.option('-sat', 
              default=250, 
              help='Set saturation [0...254]', 
              type=click.IntRange(0, 254, clamp=True))
@click.option('-i', '--info', is_flag=True)
@click.pass_context
def setlight(ctx, id, enabled, bri, hue, sat, info):
    adr = ctx.obj['ADRESS']
    def f(x):
        return {'red': 65136,
                'green': 23536,
                'yellow': 10852,
                'blue': 43253
                }.get(x, 1000) # orange default fallthrough
    payload = {'on': enabled, 'bri': bri, 'hue':f(hue), 'sat':sat}
    req = adr + '/lights/' + str(id) + '/state'
    r = requests.put(req, data=json.dumps(payload))
    if info:
        ctx.invoke(getlights)
    
    
#******************************************************************************    
@cli.command()
@click.pass_context
def getlights(ctx):
    adr =  ctx.obj['ADRESS']
    req = requests.get(adr)
    y = req.json()
    
    click.echo('*' * 80)
    
    click.secho(adr, fg='bright_green')
        
    for k in y['lights']:
        s_k = 'Light ' + k + ':'
        s_on = 'on= ' + str(y['lights'][k]['state']['on']) + '\t '
        s_bri = 'bri=' + str(y['lights'][k]['state']['bri']) + '\t '
        s_hue = 'hue=' + str(y['lights'][k]['state']['hue']) + '\t '
        s_sat = 'sat=' + str(y['lights'][k]['state']['sat'])
        click.echo(s_k + s_on + s_bri + s_hue + s_sat)    


#******************************************************************************    
@cli.command()
@click.option('-hue', 
              default = 'green', 
              help="Set Hue", 
              type=click.Choice(['blue','green','yellow','red'])
              )
@click.option('-i', '--info', is_flag=True)
@click.pass_context
def reset(ctx, hue, info):
    adr = ctx.obj['ADRESS']
    req = requests.get(adr)
    y  = req.json()

    for k in y['lights']:
        ctx.invoke(setlight, id=k, enabled=True, bri=200, sat=200, hue=hue, info = False)
    
    if info:
        ctx.invoke(getlights)
    
