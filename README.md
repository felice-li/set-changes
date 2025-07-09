This program determines what needs to be set or struck for each scene.

Input CSV files:
1. one with headers scene-name,scene-numbers,items; named "scenesets"
2. one to denote stage left vs stage right (headers are left,right), named "leftright"

For the "scenesets" CSV file, make sure the follow rules are followed:
1. If a table requires four people to carry, make sure the table has 4 entries on the spreadsheet.
2. For objects that need to be moved between scenes, denote that with an underscore (_), e.g. table_MOVE or triangle_FLIP. If the object stays in place between two scenes, put the object's name in both scenes.
3. For objects that require multiple words, uses hyphens (-) to separate them.


Output: CSV with scene-num,scene-name,set_left,strike_left,set_right,strike_right; named "moves"

An example is provided in the example_sr_sing_2025 folder. The corresponding google sheets is here: https://docs.google.com/spreadsheets/d/1V0wjXxTw5OBIRzjw-ZrrFna7Quke_vS4yxwaxnY_cOE/edit?usp=sharing. 

To format the resulting csv file into a google sheet reminiscent of the typical tech sheet, do the following:
    1. File  -> Import to import the csv file.
    2. Color the "set" and "strike" objects green and red respectively. This allows you to keep track of those objects in future manipulations.
    3. Cut and paste the columns such that the "set_left", "strike_left", "set_right", and "strike_right" columns are in one long column. In other words, stack the columns on top of each other.
    4. Split the cells such that one cell holds one set piece by selecting the stacked column and selecting Data -> Split text to columns. Choose the space separator. 
    5. Manually cut and paste the cells such that the set and strike pieces align with each set. I recommend doing this by moving the "set_left", "strike_left", "set_right", and "strike_right" chunks such that the headers are in the same row. This ensures that the actions align with each scene. Then, move cells across columns to remove white cells. However, it may be useful to keep white cells such that stage left and stage right actions are distinctly separated, mimicking the separation between members on stage left and stage right. 
    6. If the current format of having roles be spreaad across columns work (horizontal spread), you are done. Otherwise, if you prefer a vertical spread, select all relevant cells, and copy. On wherever you want the vertical spread to be, click Edit -> Paste special -> Transposed. The transposed version of whatever you copied will be pasted there.
