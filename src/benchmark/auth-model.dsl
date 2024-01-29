type user

type unit
  relations
    define member: [user]
    define parent: [unit]

type issue
  relations
    define editor: [user, unit, unit#member]
    define viewer: [user, unit, unit#member]
    define can_edit: editor or owner
    define can_view: can_edit or viewer or participant
