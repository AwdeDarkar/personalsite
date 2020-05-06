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
import { Marked } from "@ts-stack/markdown";

interface EditorProps
{
    content: ContentState;
    onContentChange: (content: ContentState) => void;
}

export interface RendererProps { content: ContentState; }
export interface RenderedEditorProps { content: string; }

class ContentState
{
    private content: string;

    constructor(initial: string)
    {
        this.content = initial;
    }

    getContent(): string
    {
        return this.content;
    }

    setContent(newcontent: string)
    {
        this.content = newcontent;
    }
}

export class RenderedEditor extends React.Component<RenderedEditorProps,
    {content: ContentState}>
{
    private content: ContentState;

    constructor(props: RenderedEditorProps)
    {
        super(props);
        this.state = {content: new ContentState(props.content)};
        this.handleContentChange = this.handleContentChange.bind(this);
    }

    handleContentChange(newContent: ContentState)
    {
        this.setState({content: new ContentState(newContent.getContent())}); 
    }

    render()
    {
        return (
        <React.Fragment>
            <div className="cell small-6">
                <div className="custom-postcomponent-editor">
                    <PostEditor
                     onContentChange={this.handleContentChange}
                     content={this.state.content}/>
                </div>
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

export class PostRenderer extends React.Component<RendererProps, {}>
{
    render()
    {
        return  <div dangerouslySetInnerHTML={
            {__html: Marked.parse(this.props.content.getContent())}
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
        this.props.onContentChange(new ContentState(target.value));
    }

    render()
    {
        return (<textarea
            onChange={this.handleChange}
            value={this.props.content.getContent()}></textarea>);
    }
}
