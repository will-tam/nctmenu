# -*- coding: utf-8 -*-

# Standard libraries import.
import collections as c


# Third libraries import.


# Projet modules import.


######################

class Sorted_according():
    """
    Choice of the sort according (see functions' name).
    """

    # Private attributes.


    # Public methods.
    def paths(self, odbin):
        """
        The path of binaries.
        @parameters : odbin = OrderedDict of binaries.
        @result : Sorted OrderedDict.
        """
        return c.OrderedDict(sorted(odbin.items(), key=lambda t: t[0]))

    def filenames(self, odbin):
        """
        The name of binaries.
        @parameters : odbin = OrderedDict of binaries.
        @result : Sorted OrderedDict.
        """
        def find_name(absolute):
            only_name = absolute[0].split("/")
            return only_name[-1]

        return c.OrderedDict(sorted(odbin.items(), key=lambda t: find_name(t)))

    def documentations_exist(self, odbin):
        """
        If the whatis doc exists.
        (Don't know if it's The Best way to do).
        @parameters : odbin = OrderedDict of binaries.
        @result : Sorted OrderedDict.
        """
        odbin = self.paths(odbin)  # 1rst, ask sort by pathes.

        with_doc = c.OrderedDict()
        without_doc = c.OrderedDict()

        # TODO: Voir à utiliser self.pathes(odbin).items() directement.
        for k, v in odbin.items():
            if v[0]:
                with_doc[k] = v
            else:
                without_doc[k] = v

        with_doc.update(without_doc)        # Concatenate the both OrderedDicts.

        return with_doc

    # Private methods.


######################

if __name__ == "__main__":
    help(My_class)
