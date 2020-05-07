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

function loadStateFromID(id: number): RenderedEditorState
{
    var serverSkills = loadSkills();

    return {
        title: "New Post",
        skillList: serverSkills,
        content: "",
        changed: false
    };
}

function saveStateToID(id: number, state: RenderedEditorState): void
{

}

function loadSkills(): skill[]
{
    return [];
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

    constructor(props: RenderedEditorProps)
    {
        super(props);
        this.state = loadStateFromID(this.props.id);
        this.handleContentChange = this.handleContentChange.bind(this);
        this.handleSave = this.handleSave.bind(this);
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

    handleSave()
    {
        // DO SAVING THINGS
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
            <div className="cell small-6">
                <TitleBar title={this.state.title} />
                <div className="custom-postcomponent-editor">
                    <PostEditor
                     onContentChange={this.handleContentChange}
                     content={this.state.content}/>
                </div>
                <SkillsSelector skillList={this.state.skillList} />
                <SaveButton
                 onSave={this.handleSave}
                 changed={this.state.changed}/>
            </div>
            <div className="cell small-6">
                <div className="custom-postcomponent-renderer">
                    <PostRenderer
                     content={this.state.content}/>
                </div>
            </div>
        </React.Fragment>);
    }
}

class TitleBar extends React.Component<TitleProps, {}>
{
    render()
    {
        return <input id="ptitle" type="text" name="title" value={this.props.title}
                placeholder="Post Title" />;
    }
}

class SkillsSelector extends React.Component<SkillsProps, {}>
{
    render()
    {
        let skillOptions: JSX.Element[] = [];
        
        this.props.skillList.forEach(function(skl: skill)
            {
                skillOptions.push(
                    <option value={this.props.skill.id}
                    selected={this.props.skill.selected}>{this.props.skill.name}</option>
                );
            }
        );

        return (
            <React.Fragment>
                <label htmlFor="skills">{`Choose this post's skill associations `}
                    (or <a href="/skills/create">{`create a new skill`}</a>)</label>
                <select id="skills" name="skills" multiple>
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
