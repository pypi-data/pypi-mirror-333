**Computational Definition**

A Statement (aka ‘Assertion’) represents a claim of purported truth as made by a particular agent,  on a particular occasion.

    **Information Model**

Some Statement attributes are inherited from :ref:`InformationEntity`.

    .. list-table::
       :class: clean-wrap
       :header-rows: 1
       :align: left
       :widths: auto

       *  - Field
          - Type
          - Limits
          - Description
       *  - id
          - string
          - 1..1
          - The 'logical' identifier of the entity in the system of record, e.g. a UUID. This 'id' is  unique within a given system. The identified entity may have a different 'id' in a different  system, or may refer to an 'id' for the shared concept in another system (e.g. a CURIE).
       *  - label
          - string
          - 0..1
          - A primary label for the entity.
       *  - description
          - string
          - 0..1
          - A free-text description of the entity.
       *  - extensions
          - `Extension <../../gks-common/core.json#/$defs/Extension>`_
          - 0..m
          -
       *  - type
          - string
          - 1..1
          -
       *  - specifiedBy
          - :ref:`Method` | `IRI <../../gks-common/core.json#/$defs/IRI>`_
          - 0..1
          - A :ref:`Method` that describes all or part of the process through which the information was generated.
       *  - contributions
          - :ref:`Contribution`
          - 0..m
          -
       *  - isReportedIn
          - :ref:`Document` | `IRI <../../gks-common/core.json#/$defs/IRI>`_
          - 0..m
          - A document in which the information content is expressed.
       *  - recordMetadata
          - None
          - 0..1
          -
       *  - subject
          - _Not Specified_
          - 1..1
          - The subject of the Statement.
       *  - predicate
          - string
          - 0..1
          - The predicate of the Statement.
       *  - object
          - _Not Specified_
          - 0..1
          - The object of the Statement.
       *  - qualifiers
          - object
          - 0..1
          - Additional, optional properties that may qualify the Statement.
       *  - direction
          - string
          - 1..1
          - The direction of this Statement with respect to the predicate.
       *  - strength
          - `Coding <../../gks-common/core.json#/$defs/Coding>`_ | `IRI <../../gks-common/core.json#/$defs/IRI>`_
          - 0..1
          - The overall strength of support for the Statement based on all evidence assessed.
