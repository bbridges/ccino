class Event(object):
    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs


class Evented(object):
    def __init__(self):
        """Create an Evented object."""
        self._func_dict = {}

    def on(self, event, func):
        """Register a function to run on an event.

        Whenever `event` gets emitted, `func` will be run immediately
        after. Functions that have been registered first will run
        before functions registered afterwards.

        Args:
            event: A string for the event name.
            func: The function to run on the event.
        """

        if not event in self._func_dict:
            self._func_dict[event] = []

        self._func_dict[event].append((func, False))

    def once(self, event, func):
        """Register a function to run on an event once.

        Whenever `event` gets emitted, `func` will only be run
        immediately the first time the event is emitted, after it
        will be removed from running. Functions that have been
        registered first will run before functions registered
        afterwards.

        Args:
            event: A string for the event name.
            func: The function to run once for the event.
        """

        if not event in self._func_dict:
            self._func_dict[event] = []

        self._func_dict[event].append((func, True))

    def remove_listener(self, func):
        """Stop a function from running on an event.

        Note that if `func` is registered to multiple events it will
        remove it from running from all events.

        Args:
            func: The function to remove

        Returns:
            True if it removed the function, False if it was not
            found.
        """

        removed = False

        for event in self._func_dict:
            func_list = self._func_dict[event]

            i = 0

            while i < len(func_list):
                curr_func = func_list[i][0]

                if curr_func is func:
                    del func_list[i]

                    removed = True
                else:
                    i += 1

        return removed

    def emit(self, event, *args, **kwargs):
        """Emit a event and run the associated functions.

        The registered functions are run in the order that they were
        added.

        IF no registered functions are called, an 'Evented.silent'
        event will be emitted with an Event object containing the
        silent event name and its arguments and keyword arguments.
        If no function is registered to an 'Evented.*' event, another
        'Evented.silent' event will not be emitted.

        If one of the registered functions throws an error, an
        'Evented.error' event will be emitted with the error as the
        only argument. If a function throws an error when listening
        to the 'Evented.error' event is emitted, another
        'Evented.error' event will not be emitted.

        Args:
            event: The string for the event name.
            *args: The arguments to be passed to the functions.
            **kwargs: The keyword arguments to be passed to the
                functions.
        """

        if not event in self._func_dict or len(self._func_dict[event]) == 0:
            if not event.startswith('Evented.'):
                self.emit('Evented.silent', Event(event, args, kwargs))

            return

        func_list = self._func_dict[event]

        i = 0

        while i < len(func_list):
            curr_func, delete = func_list[i]

            try:
                curr_func(*args, **kwargs)
            except Error as e:
                if not event == 'Evented.error':
                    self.emit('Evented.error', e)

            if delete:
                del func_list[i]
            else:
                i += 1
