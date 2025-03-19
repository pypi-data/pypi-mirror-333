from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import os
import shutil
import logging

class TCCPDocsStylesPlugin(BasePlugin):
    config_scheme = (
        ('style_dir', config_options.Dir(exists=True)),
        ('add_favicon', config_options.Type(bool, default=True)),
        ('add_logo', config_options.Type(bool, default=True)),
        ('add_material_palette', config_options.Type(bool, default=True)),
        ('light_scheme', config_options.Type(str, default='modus')),
        ('dark_scheme', config_options.Type(str, default='slate')),        
    )

    def __init__(self):
        self.logger = logging.getLogger('mkdocs.plugins.tccp-docs-styles')

    def on_config(self, config):
        """
        Add extra CSS files to the config
        """
        self.logger.info("TCCPDocsStylesPlugin: Configuring...")
        
        # Configure the Material theme palette if enabled
        if self.config.get('add_material_palette', True) and 'theme' in config:

            # Add favicon and logo
            if self.config.get('add_favicon', True):
                if 'theme' not in config:
                    config['theme'] = {}
                if isinstance(config['theme'], str):
                    config['theme'] = {'name': config['theme']}
                config['theme']['favicon'] = 'assets/logo360.svg'
                self.logger.info(f"TCCPDocsStylesPlugin: Added Favicon")

            if self.config.get('add_logo', True):
                if 'theme' not in config:
                    config['theme'] = {}
                if isinstance(config['theme'], str):
                    config['theme'] = {'name': config['theme']}
                config['theme']['logo'] = 'assets/trimble-logo.svg'
                self.logger.info(f"TCCPDocsStylesPlugin: Added Logo")

            # Make sure we're dealing with Material theme
            if config['theme'].get('name') == 'material':
                light_scheme = self.config.get('light_scheme', 'modus')
                dark_scheme = self.config.get('dark_scheme', 'slate')
                
                # Set palette configuration
                palette = [
                    {
                        'media': '(prefers-color-scheme: light)',
                        'scheme': light_scheme,
                        'toggle': {
                            'icon': 'material/brightness-7',
                            'name': 'Switch to dark mode'
                        }
                    },
                    {
                        'media': '(prefers-color-scheme: dark)',
                        'scheme': dark_scheme,
                        'toggle': {
                            'icon': 'material/brightness-4',
                            'name': 'Switch to system preference'
                        }
                    }
                ]
                
                # Update the theme configuration
                if 'palette' not in config['theme']:
                    config['theme']['palette'] = palette
                self.logger.info(f"TCCPDocsStylesPlugin: Added Material theme palette configuration")
 
        # Get the style directory from the config or use a default
        style_dir = self.config.get('style_dir')
        if style_dir is None:
            style_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles')
        self.logger.info(f"Style directory: {style_dir}")

        # Make sure the styles will be included in the output
        if 'extra_css' not in config:
            config['extra_css'] = []
        
        # Add your main CSS file
        config['extra_css'].append('css/modus-styles.css')
        
        return config
    
    def on_post_build(self, config):
        """
        Copy the CSS files to the site directory after the build
        """
        style_dir = self.config.get('style_dir')
    
        # If style_dir is None, use a default path relative to the plugin directory
        if style_dir is None:
            style_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles')
        
        output_dir = os.path.join(config['site_dir'], 'css')

        # Create the CSS directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Copy your main CSS file and all imported files
        css_files = ['modus-styles.css', 'admonition.css', 'colors.css', 'announcement.css']
        for css_file in css_files:
            src = os.path.join(style_dir, css_file)
            dst = os.path.join(output_dir, css_file)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                self.logger.info(f"Copied {css_file} to {output_dir}")
            else:
                self.logger.warning(f"CSS file not found: {src}")
        
        # Handle asset files (logos)
        assets_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        assets_output_dir = os.path.join(config['site_dir'], 'assets')
        # Create the assets directory if it doesn't exist
        os.makedirs(assets_output_dir, exist_ok=True)
        
        # Copy the SVG logo files
        svg_files = ['logo360.svg', 'trimble-logo.svg']
        for svg_file in svg_files:
            src = os.path.join(assets_src_dir, svg_file)
            dst = os.path.join(assets_output_dir, svg_file)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                self.logger.info(f"Copied {svg_file} to {assets_output_dir}")
            else:
                self.logger.warning(f"SVG file not found: {src}")

        return config