# Sublime SelectNext plugin

Based on [AppendSelection](https://github.com/shagabutdinov/sublime-append-selection.git) sublime plugin. I made it more closely imitate the behavior of a visual studio extension I'm used to.


### Installation

Clone to `sublime-text/Packages/SelectNext`.


### Features

1. Select text forward
2. Select text backward
3. Select word forward
4. Select word forward
5. Undo the latest selection
6. Clear all selections so that the latest selection remains


### Usage

Select a text or position cursor on top of word that should be selected several times. Hit keyboard shortcuts to add next or previous occurence of word to cursors.


### Commands

| Description          | Keyboard shortcuts | Command palette             |
|----------------------|--------------------|-----------------------------|
| Select next          | ctrl+shift+down    | SelectNext: next match      |
| Select previous      | ctrl+shift+up      | SelectNext: previous match  |
| Select next word     | ctrl+alt+down      | SelectNext: next word       |
| Select previous word | ctrl+alt+shift+up  | SelectNext: previous word   |
| Undo selection       | ctrl+alt+shift+z   | SelectNext: undo latest     |
| Clear selection      | escape             | SelectNext: clear selection |


### Dependencies

None
