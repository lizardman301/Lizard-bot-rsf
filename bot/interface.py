# Local imports
from commands import commands, challonge, edit # Bring in all commands
from commands.utilities import (get_callbacks, read_db, stat_up, read_disable) # Bring in some utilities to help the process

# Yaksha
class Interface():

    # Yaksha
    # Initialize Interface with all our nice defaults
    def __init__(self, admin_commands, help):
        self._func_mapping = {} # Map for future reference
        self._modules = [commands, challonge, edit] # Stores the reference to each .py we have command functions in
        self.remap_functions() # Map functions for reference by command name
        self.admin_commands = admin_commands # Bring over the admin commands
        self.help = help # Bring over help info

    # Yaksha
    def remap_functions(self):
        '''
        Utilities.get_callbacks() returns a dictionary mapping of
        each command with the name of the function to be called.

        The name of the function is replaced by this function
        with a reference to the function and the class it belongs
        to. This is later used by self.call_command when handling
        messages.
        '''
        name_mapping = get_callbacks()

        for key, value in name_mapping.items():
            func_name = value[0]
            module_name = value[1]
            # Go through the imported modules to determine which
            # module the class belongs to.
            for module in self._modules:
                if module.__name__ != module_name:
                    continue
                else:
                    func_ref = getattr(module, func_name)

                    # Replace the function name with a tuple
                    # containing a reference to the function and
                    # the class name. The class name will be used
                    # get the correct class from self._class_mapping.
                    self._func_mapping[key] = func_ref
                    # We found the module so there is no need for further
                    # iterations.
                    break

    # Yaksha
    async def call_command(self, command, msg, user, channel, *args, **kwargs):
        '''
        Determines which function to call from the func_mapping
        dict using the command arg as the key.
        '''
        # First check if the command is disabled
        if self._func_mapping[command].__name__ in read_disable(kwargs['guild']):
            return "**{0}** has been disabled in this server.".format(command)

        # Second check if the user is allowed to call this
        # function.
        if await self.user_has_permission(user, command, kwargs['guild']):
            # Keyword args that could be deferred until now
            if self._func_mapping[command].__name__ == 'help_lizard':
                kwargs['help'] = self.help
            elif self._func_mapping[command].__name__ in ['disable','enable','stats']:
                kwargs['func_map'] = self._func_mapping

            # Try to complete the command's function
            try:
                result = await self._func_mapping[command](command, msg, user, channel, *args, **kwargs)
                stat_up(self._func_mapping[command].__name__) # Increment command's stat after it is successful
                return result
            except:
                raise # Re-raise same error
        else:
            # No permission
            return "You do not have permissions to access the command: " + command

    async def user_has_permission(self, user, command, id):
        '''
        Performs various checks on the user and the
        command to determine if they're allowed to use it.
        '''
        # Check if the user is an admin and
        # if the command is an admin command.
        if command in self.admin_commands:
            botrole = read_db('guild', 'botrole', id)

            # If botrole is not set, allow the command
            if not botrole:
                return True

            # Find if the user has botrole
            for role in user.roles:
                if role.id == botrole:
                    return True
            return False

        # User passed all the tests so they're allowed to
        # call the function.
        return True