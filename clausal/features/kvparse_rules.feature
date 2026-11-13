Feature: Kvparse rules
  Rule lines of the project `kvparse` (projects.yaml).

  # >>> pack validated-input@1: written by `python3 -m clausal pack instantiate` from packs/validated-input/pack.yaml with the
  # bindings of features/kvparse_rules.pack.validated-input.yaml. Plain Rule lines, compiled like any other; the @pack tags are read by nothing in the pipeline.
  # Members of the pack that are NOT stated here are listed in the bindings file and by `python3 -m clausal pack check`.

  # VI-1: a parse gives an answer for every input (no panic, no endless loop, in the model)
  @id:vi_1 @pack:validated-input@1 @pack-rule:VI-1 @expect-unproved
  Rule: A parse always answers

  # VI-2: nothing outside the format is accepted
  @id:vi_2 @pack:validated-input@1 @pack-rule:VI-2 @expect-unproved
  Rule: A parse is accepted only if the message is well-formed

  # VI-3: everything in the format is accepted (progress: excludes reject-everything)
  @id:vi_3 @pack:validated-input@1 @pack-rule:VI-3 @expect-unproved
  Rule: A parse for which the length of the message is at most the parser's size limit is accepted whenever the message is well-formed

  # VI-4: oversize input is rejected
  @id:vi_4 @pack:validated-input@1 @pack-rule:VI-4
  Rule: A parse is accepted only if the length of the message is at most the parser's size limit

  # VI-5: the parsed value has a bounded number of items
  @id:vi_5 @pack:validated-input@1 @pack-rule:VI-5
  Rule: For a parse, the number of fields of the result is at most the field limit

  # VI-6: input outside the format is rejected and changes nothing (the second half says something only of a parser with state)
  @id:vi_6 @pack:validated-input@1 @pack-rule:VI-6 @expect-unproved
  Rule: A parse for which the message is not well-formed is rejected and changes nothing

  # VI-7b: the accepted input is exactly the encoding of the parsed value (excludes a wrong or default value and a dropped field)
  @id:vi_7b @pack:validated-input@1 @pack-rule:VI-7b @expect-unproved
  Rule: For an accepted parse, the encoding of the result is the bytes of the message

  # VI-8: the stated policy for items the format does not define
  @id:vi_8 @pack:validated-input@1 @pack-rule:VI-8 @expect-unproved
  Rule: A parse is accepted only if every field of the message is a known field

  # VI-9: the stated policy for a repeated key
  @id:vi_9 @pack:validated-input@1 @pack-rule:VI-9 @expect-unproved
  Rule: A parse is accepted only if no key of the message is repeated in the message

  # VI-10: the answer is the reference's for every input (pins everything; costs a full signed definition of the format)
  @id:vi_10 @pack:validated-input@1 @pack-rule:VI-10 @expect-unproved
  Rule: A parse agrees with the reference parse

  # <<< pack validated-input@1
