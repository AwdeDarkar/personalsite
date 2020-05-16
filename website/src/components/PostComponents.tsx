/*
 * PostComponents
 * ==============================================================================================
 *
 * Components for writing end rendering blog posts
 *
 * ----------------------------------------------------------------------------------------------
 * 
 * **Created**
 *    2020-05-01
 * **Author**
 *    Ben Croisdale
 * **Copyright**
 *    This software is Free and Open Source for any purpose
 */

import * as React from "react";
import { Marked, Renderer } from "@ts-stack/markdown";
import { highlight } from "highlight.js";
import * as $ from "jquery";
import "foundation-sites";

interface EditorProps
{
    content: string;
    onContentChange: (content: string) => void;
}

interface SaveButtonProps
{
    changed: boolean;
    onSave: (event: React.MouseEvent<HTMLButtonElement>) => void
};

interface TitleProps
{
    title: string;
    onContentChange: (title: string) => void;
};

interface skill
{
    name: string;
    id: number;
    selected: boolean;
};

interface SkillsProps
{
    skillList: skill[];
    onContentChange: (skills: skill[]) => void;
};

export interface RendererProps { content: string; }
export interface RenderedEditorProps { id?: number; }

interface RenderedEditorState
{
    title: string;
    skillList: skill[];
    content: string;
    changed: boolean;
}

function loadStateFromID(id: number, editor: RenderedEditor)
{
    if (id === -1)
    {
        editor.state = {
            title: "New Post",
            skillList: [],
            content: "",
            changed: false
        };
    }
    else
    {
        editor.state = {
            title: "loading...",
            skillList: [],
            content: "",
            changed: false
        };
        $.post({
            url: "/skills/api",
            data: {
                "action": "read",
                "kind": "post",
                "post-id": id
            },
            success: function(data: any, textStatus: string, jqxhr: any)
            {
                editor.setState({
                    title: data["title"],
                    skillList: [],
                    content: data["content"],
                    changed: false
                });
            }
        });
    }
    loadSkills(id, function(skills: skill[]){
        editor.setState({
            title: editor.state.title,
            skillList: skills,
            content: editor.state.content,
            changed: editor.state.changed
        });
    });
}

function saveStateToID(id: number, state: RenderedEditorState,
    onCreate: (newid: number) => void): void
{
    var skill_ids: number[] = [];
    state.skillList.forEach(function(skl: skill){
        if(skl.selected) { skill_ids.push(skl.id); }
    });
    console.log(skill_ids);
    console.log(state.skillList);

    if (id === -1)
    {
        $.post({
            url: "/skills/api",
            data: {
                "action": "create",
                "kind": "post",
                "title": state.title,
                "content": state.content,
                "skill-ids": skill_ids
            },
            success: function(data: any, textStatus: string, jqxhr: any)
            {
                onCreate(Number(data["new-id"]));
            }
        });
    }
    else
    {
        $.post({
            url: "/skills/api",
            data: {
                "action": "modify",
                "kind": "post",
                "post-id": id,
                "title": state.title,
                "content": state.content,
                "skill-ids": skill_ids
            },
        });
    }
}

function loadSkills(id: number, setSkills: (skills: skill[]) => void)
{
    $.post({
        url: "/skills/api",
        data: {
            "action": "read",
            "kind": "skill",
            "post-id": id,
        },
        success: function(data: any, textStatus: string, jqxhr: any)
        {
            var skills: skill[] = [];
            console.log(data);
            var rawskills = data.skills;
            rawskills.forEach(function(rawskill: any) {
                skills.push({
                    name: rawskill.name,
                    id: rawskill.id,
                    selected: rawskill.selected
                });
            });
            setSkills(skills);
        }
    });
}

/*
 * Make the server generate a new post ID to save to
 */
function getNewID(): number
{
    return null;
}

export class RenderedEditor extends React.Component<RenderedEditorProps, RenderedEditorState>
{
    private content: string;
    private changed: boolean;
    private id: number;

    constructor(props: RenderedEditorProps)
    {
        super(props);
        this.id = this.props.id;
        loadStateFromID(this.id, this);
        this.handleContentChange = this.handleContentChange.bind(this);
        this.handleTitleChange = this.handleTitleChange.bind(this);
        this.handleSkillsChange = this.handleSkillsChange.bind(this);
        this.handleSave = this.handleSave.bind(this);
    }

    componentDidMount()
    {
        $(document).foundation();
    }

    componentDidUpdate()
    {
        $(document).foundation();
    }

    handleContentChange(newContent: string)
    {
        this.setState({
            title: this.state.title,
            skillList: this.state.skillList,
            content: newContent,
            changed: true
        });
    }

    handleTitleChange(newTitle: string)
    {
        this.setState({
            title: newTitle,
            skillList: this.state.skillList,
            content: this.state.content,
            changed: true
        });
    }

    handleSkillsChange(newSkills: skill[])
    {
        this.setState({
            title: this.state.title,
            skillList: newSkills,
            content: this.state.content,
            changed: true
        });
    }

    handleSave()
    {
        var setnewid = this.id;
        saveStateToID(this.id, this.state, function(newid: number){
            setnewid = newid;
        });
        this.id = setnewid;
        this.setState({
            title: this.state.title,
            skillList: this.state.skillList,
            content: this.state.content,
            changed: false
        });
    }

    render()
    {
        return (
        <React.Fragment>
            <ul className="tabs" data-tabs id="renderedEditorTabs">
                <li className="tabs-title is-active"><a href="#editor"
                    aria-selected="true">Editor</a></li>
                <li className="tabs-title"><a data-tabs-target="renderer"
                    href="#renderer">Renderer</a></li>
            </ul>
            <div className="tabs-content" data-tabs-content="renderedEditorTabs">
                <div className="tabs-panel is-active" id="editor">
                    <TitleBar title={this.state.title}
                     onContentChange={this.handleTitleChange}/>
                    <div className="custom-postcomponent-editor">
                        <PostEditor
                         onContentChange={this.handleContentChange}
                         content={this.state.content}/>
                    </div>
                    <SkillsSelector skillList={this.state.skillList}
                     onContentChange={this.handleSkillsChange}/>
                    <SaveButton
                     onSave={this.handleSave}
                     changed={this.state.changed}/>
                </div>
                <div className="tabs-panel" id="renderer">
                    <div className="custom-postcomponent-renderer">
                        <PostRenderer
                         content={this.state.content}/>
                    </div>
                </div>
            </div>
        </React.Fragment>);
    }
}

class TitleBar extends React.Component<TitleProps, {}>
{
    constructor(props: TitleProps)
    {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    private handleChange(event: React.SyntheticEvent<HTMLInputElement>)
    {
        let target = event.target as HTMLTextAreaElement;
        this.props.onContentChange(target.value);
    }

    render()
    {
        return <input id="ptitle" type="text" name="title" value={this.props.title}
                onChange={this.handleChange}
                placeholder="Post Title" />;
    }
}

class SkillsSelector extends React.Component<SkillsProps, {}>
{
    constructor(props: SkillsProps)
    {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    private handleChange(event: React.SyntheticEvent<HTMLSelectElement>)
    {
        let target = event.target as HTMLSelectElement;
        let skills: skill[] = [];
        for(var i = 0; i < target.options.length; i++)
        {
            let option = target.options[i];
            skills.push({
                name: option.innerHTML,
                id: Number(option.value),
                selected: option.selected
            });
        }
        this.props.onContentChange(skills);
    }

    render()
    {
        let skillOptions: JSX.Element[] = [];
        var self: SkillsSelector = this;
        this.props.skillList.forEach(function(skl: skill)
            {
                skillOptions.push(
                    <option value={skl.id}
                     selected={skl.selected}>{skl.name}</option>
                );
            }
        );

        return (
            <React.Fragment>
                <label htmlFor="skills">{`Choose this post's skill associations `}
                    (or <a href="/skills/create">{`create a new skill`}</a>)</label>
                <select onChange={self.handleChange} id="skills" name="skills" multiple>
                    {skillOptions}
                </select>
            </React.Fragment>
        );
    }
}

class SaveButton extends React.Component<SaveButtonProps, {}>
{
    render()
    {
        if (this.props.changed)
        {
            return <button onClick={this.props.onSave}
                    type="button" className="warning button">Save</button>;
        }
        else
        {
            return <button onClick={this.props.onSave}
                    type="button" className="success button">Save</button>;
        }
    }
}

export class PostRenderer extends React.Component<RendererProps, {}>
{
    render()
    {
        Marked.setOptions({
            highlight: function(code: string, lang: string): string
            {
                return "<div title='" + lang + "' class='code-block'>" +
                    highlight(lang, code).value +
                    "</div>";
            }
        });

        return  <div dangerouslySetInnerHTML={
            {__html: Marked.parse(this.props.content)}
        } />;
    }
}

class PostEditor extends React.Component<EditorProps, {}>
{
    constructor(props: EditorProps)
    {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    private handleChange(event: React.SyntheticEvent<HTMLTextAreaElement>)
    {
        let target = event.target as HTMLTextAreaElement;
        this.props.onContentChange(target.value);
    }

    render()
    {
        return (<textarea
            onChange={this.handleChange}
            value={this.props.content}></textarea>);
    }
}
