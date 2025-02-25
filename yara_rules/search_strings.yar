rule FindSpecificString
{
    meta:
        description = "This rule looks for a specific string (case-insensitive)"
        author = "Hendrik"
        date = "2024-12-30"

    strings:
        $my_string = "HalloWelt" nocase

    condition:
        $my_string
}
