import argparse
import chemlib
import discord
from discord.ext import commands
import cogs.utils.error

from rdkit import rdBase, Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem.Draw import rdMolDraw2D
from IPython.display import SVG
import pubchempy as pcp

from rdkit.Chem import PandasTools
import pandas as pd
import numpy as np
from io import BytesIO
import copy
from PIL import Image, ImageFilter
from cairosvg import svg2png
import argparse


def generate_image(mol, size):

    image_data = BytesIO()
    view = rdMolDraw2D.MolDraw2DSVG(size[0], size[1])
    tm = rdMolDraw2D.PrepareMolForDrawing(mol)

    view.DrawMolecule(tm)
    view.FinishDrawing()
    svg = view.GetDrawingText()
    SVG(svg.replace('svg:', ''))
    svg2png(bytestring=svg, write_to='output.png')
    img = Image.open('output.png')
    img.save(image_data, format='PNG')

    return image_data

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-cmpd', type=str)

cmpd_parser = argparse.ArgumentParser(parents=[parser])
cmpd_parser.add_argument('--amount', type=str)
cmpd_parser.add_argument('--composition', type=str)
cmpd_parser.add_argument('--structural-formula', nargs='?', const=0)
cmpd_parser.add_argument('--get-smiles', nargs='?', const=0)

class Compounds(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.group(name = 'cmpd', aliases = ['compound', 'comp'])
    async def cmpd(self, ctx, *args):
        try:
            emoji = u"\u2705"
            cmd = vars(cmpd_parser.parse_args(['-cmpd'] + list(args)))
            print(cmd)
            print(cmd['cmpd'])
          
            if cmd['get_smiles'] is not None:
                print('LINE56\n')
                benzene = pcp.get_compounds(cmd['cmpd'], 'name')
                if len(benzene) == 1: benzene = benzene[0]
                smiles = benzene.canonical_smiles
                print(smiles)  # 'C1=CC=CC=C1'
                cmpd = cmd['cmpd']
                embed = discord.Embed(title=f'{cmpd} SMILES', color=0x7b2fde)
                embed.add_field(name = "smiles", value = f"{smiles}", inline = False)
                await ctx.message.add_reaction(emoji)
                await ctx.send(embed = embed)
                return
          
            compound = chemlib.Compound(cmd['cmpd'])
            print(compound)
            embed = discord.Embed(title=f'{compound.formula} Properties', color=0x7b2fde)
            print('LINE28.\n')
            if compound.molar_mass() == 0: raise ValueError
            embed.add_field(name = "Molar Mass", value = str(compound.molar_mass()) + ' g/mol', inline=False)
            print('LINE31\n')
          
            if cmd['amount'] is not None:
                amt = cmd['amount']
                if 'g' in amt: amts = compound.get_amounts(grams = float(amt[:-1]))
                elif 'mol' in amt: amts = compound.get_amounts(moles = float(amt[:-3]))
                else: amts = compound.get_amounts(molecules = float(amt[:-9]))
                for field in amts:
                    if field not in ('compound', 'Compound'):
                        embed.add_field(name = field.capitalize(), value=amts[field], inline=True)
            
            if cmd['composition'] is not None:
                elem = cmd['composition']
                embed.add_field(name = f"% composition of {elem}", value = compound.percentage_by_mass(elem), inline=False)
            
            if cmd['structural_formula'] is not None:
                print('LINE56\n')
                # benzene = pcp.get_compounds('benzene', 'name')
                # if len(benzene) == 1: benzene = benzene[0]
                # smiles = benzene.canonical_smiles
                smiles = cmd['cmpd']
                print(smiles)  # 'C1=CC=CC=C1'
                mol_ben = Chem.MolFromSmiles(smiles)
                print(type(mol_ben))  #
                print(Chem.MolToMolBlock(mol_ben))
                
                #Draw.MolToImage(mol_ben) # doesn't work in replit
                generate_image(mol_ben, size=(300, 300))
                Draw.MolToFile(mol_ben, 'output.svg')
                files = [
                    discord.File('output.svg'),
                    discord.File('output.png')
                ]
                embed.set_thumbnail(url = 'attachment://output.png')
                await ctx.message.add_reaction(emoji)
                await ctx.send(files = files, embed = embed)
                return
              
            if cmd['get_smiles'] is not None:
                print('LINE56\n')
                benzene = pcp.get_compounds(cmd['cmpd'], 'name')
                if len(benzene) == 1: benzene = benzene[0]
                smiles = benzene.canonical_smiles
                print(smiles)  # 'C1=CC=CC=C1'
                embed.add_field(name = "smiles", value = f"{smiles}", inline = False)
              
        except:
            emoji = "❌"
            embed = cogs.utils.error.Error(f"Error parsing the inputted formula.", example= "-cmpd C6H12O6\n-cmpd H2O2 --am 25g\n-cmpd AlCl3 --am 3.5mol\n-cmpd H2S --comp S")
        
        await ctx.message.add_reaction(emoji)
        await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Compounds(bot))