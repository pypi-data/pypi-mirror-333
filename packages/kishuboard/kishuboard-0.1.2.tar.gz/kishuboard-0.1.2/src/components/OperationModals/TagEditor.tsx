import React, {useState} from "react";
import {Modal, Input, Button, message} from "antd";

export interface TagEditorProps {
    isModalOpen: boolean;
    setIsModalOpen: any;
    submitHandler: (newTagName:string, oldTagName:string|undefined) => Promise<void>;
    selectedHistoryID?: string;
    tagToBeEdit: string|undefined;
    setTagToBeEdit: any;
}

function TagEditor(props: TagEditorProps) {
    const [loading, setLoading] = useState(false);
    const [content, setContent] = useState("");

    async function handleOk() {
        setLoading(true);
        try {
            await props.submitHandler(content,props.tagToBeEdit);
            setLoading(false);
            message.info(props.tagToBeEdit?"Edit tag succeed":"Create tag succeed");
            props.setTagToBeEdit(undefined);
            props.setIsModalOpen(false);
        } catch (e) {
            setLoading(false);
            if (e instanceof Error) {
                message.error("tag edit error" + e.message);
            }
        }
    }

    const handleCancel = () => {
        props.setIsModalOpen(false);
        props.setTagToBeEdit(undefined);
    };

    const handleChange: any = (event: any) => {
        setContent(event.target.value);
    };

    return (
        <Modal
            title={props.tagToBeEdit?"Edit tag name for tag " + props.tagToBeEdit!:"Create a tag for the selected history"}
            open={props.isModalOpen}
            onOk={handleOk}
            onCancel={handleCancel}
            footer={[
                <Button key="back" onClick={handleCancel}>
                    Return
                </Button>,
                <Button
                    key="submit"
                    type="primary"
                    loading={loading}
                    onClick={handleOk}
                >
                    Submit
                </Button>,
            ]}
        >
            <Input onChange={handleChange} value={content}/>
        </Modal>
    );
}

export default TagEditor;
