import {Cell} from "./Cell";
import {Commit, CommitDetail} from "./Commit";
import {Variable} from "./Variable";
import {Session} from "./Session";
import {DiffCodeHunk} from "./DiffHunk";
import {DiffCodeDetail} from "./DiffCommitDetail";
import {logger} from "../log/logger";
import {VariableVersionCompare} from "./VariableVersionCompare";

export function parseList(object: any):Session[]{
    logger.silly("session list from backend",object)
    const _sessions = object["sessions"];
    return _sessions.map(
        (item: any) => (
            {
                NotebookID: item["notebook_key"],
                kernelID: item["kernel_id"],
                notebookPath: item["notebook_path"],
                isAlive: item["is_alive"],
            }
        ) as Session
    )
}

//parse and sort the data from backend
export function parseCommitGraph(object: any) {
    // logger.silly("git graph from backend", object)
    console.log("git graph from backend", object)
    const items = object["commits"];
    let commits: Commit[] = items.map(
        (item: any) =>
            ({
                oid: item["oid"],
                // branchIds: item["branch_ids"],
                branchIds: item["branches"],
                timestamp: item["timestamp"],
                parentOid: item["parent_oid"],
                nbParentOid: item["nb_parent_oid"],
                tags: item["tags"],
                codeVersion: item["code_version"],
                variableVersion: item["varset_version"],
                message: item["message"].replace("Auto-commit after executing",""),
                belongCodeBranchIds:new Set<string>(),
                belongVarBranchIds:new Set<string>()
            }) as Commit,
    );
    const currentHead = object["head"]["commit_id"];
    const currentHeadBranch = object["head"]["branch_name"];
    const currentNBHead = object["nb_head"];
    //sorted by time, from newest to oldest
    commits.sort((a, b) => {
        const timestampA = new Date(a.timestamp).getTime();
        const timestampB = new Date(b.timestamp).getTime();
        return timestampB - timestampA;
    });
    calBelongBranches(commits, currentHead, currentNBHead)
    commits = commits.filter((commit)=> commit.belongCodeBranchIds.size != 0 || commit.belongVarBranchIds.size != 0)

    return {
        commits: commits,
        currentHead: currentHead,
        currentNBHead: currentNBHead,
        currentHeadBranch: currentHeadBranch,
    };
}

export function parseCommitDetail(json: any) {
    // logger.silly("commit detail from backend",json)
    const item = json["commit"];
    let commit:Commit = {
        codeVersion: item["code_version"],
        variableVersion: item["variable_version"],
        oid: item["oid"],
        timestamp: item["timestamp"],
        parentOid: item["parent_oid"],
        nbParentOid: item["nb_parent_oid"],
        branchIds: item["branches"],
        tags: item["tags"],
        message: item["message"],
        belongVarBranchIds: new Set<string>(),
        belongCodeBranchIds: new Set<string>(),
    }

    const commitDetail: CommitDetail = {
        commit: commit,
        codes: json["cells"].map(
            (item: any) =>
                ({
                    content: item["content"],
                    execNum: item["exec_num"] === "None" ? "-1" : item["exec_num"],
                    type: item["cell_type"],
                    output:item["output"]
                }) as Cell,
        ),
        variables: json["variables"].map((variable: any) =>
            recursiveGetVariable(variable),
        ).sort((a: Variable, b: Variable) => {
            return a.type==="module" ? 1 : -1
        }),
        // historyExecCells: json["cells"]
        historyExecCells: json["executed_cells"].map(
            (item: any,idx:number) => ({
                content: item,
                execNum: "-1",
                type: "code",
                output:json["executed_outputs"][idx.toString()]
            }) as Cell
        ).reverse(),
    };
    return commitDetail;
}

function recursiveGetVariable(item: any): Variable {
    if (!item["children"] || item["children"].length === 0) {
        return {
            key: item["variable_name"],
            variableName: item["variable_name"],
            state: (item["state"] as string).replaceAll("\n", "\\n"),
            type: item["type"],
            size: item["size"],
            html: item["html"],
        } as Variable;
    } else {
        return {
            key: item["variable_name"],
            variableName: item["variable_name"],
            state: (item["state"] as string).replaceAll("\n", "\\n"),
            type: item["type"],
            size: item["size"],
            html: item["html"],
            children: item["children"].map((child: any) =>
                recursiveGetVariable(child),
            ),
        } as Variable;
    }
}

export function parseCodeDiff(json: any) {
    logger.silly("diff from backend",json)
    const _notebook_cells_diff = json["notebook_cells_diff"];
    const _executed_cells_diff = json["executed_cells_diff"];
    let notebookCellDiffHunks: DiffCodeHunk[] = _notebook_cells_diff.map((item: any) => parseDiffHunk(item));
    let executedCellDiffHunks: DiffCodeHunk[] = _executed_cells_diff.map((item: any) => parseDiffHunk(item)).reverse();
    return {
        notebookCellDiffHunks: notebookCellDiffHunks,
        executedCellDiffHunks: executedCellDiffHunks
    } as DiffCodeDetail;
}

export function parseVarDiff(json: any): VariableVersionCompare[]{
    //variable will be sorted by priority, the smaller the priority, the higher the priority
    let priorityMap: Map<string, number> = new Map([
        ["both_different_version", 0],
        ["destination_only", 1],
        ["origin_only", 2],
        ["both_same_version", 3],
    ]);
    let variable_version_compares = json["var_diff_compares"];
    variable_version_compares.sort((a: any,b: any) => {return priorityMap.get(a["option"])!
    - priorityMap.get(b["option"])!})
    return variable_version_compares.map((item: any) => {
        return {variableName: item["variable_name"],
            option: item["option"]} as VariableVersionCompare
    })
}

function parseDiffHunk(json: any) {
    const _option = json["option"];
    const _content = json["content"];
    const _sub_diff_hunks = json["sub_diff_hunks"];
    return {
        option: _option,
        content: _content,
        subDiffHunks: _sub_diff_hunks?.map((item: any) => parseDiffHunk(item))
    } as DiffCodeHunk;
}

function calBelongBranches(commits:Commit[],currentHead:string, currentNBHead:string){
    let commit:Commit
    let varPCommit:Commit
    let nbPCommit:Commit
    for (let i = 0; i < commits.length; i++){
        commit = commits[i]
        commit.branchIds.forEach((branchID) => {
            commit.belongVarBranchIds.add(branchID)
            commit.belongCodeBranchIds.add(branchID)
        })
        if(commit.oid === currentHead){
            commit.belongVarBranchIds.add("var_head")
        }
        if(commit.oid === currentNBHead){
            commit.belongCodeBranchIds.add("nb_head")
        }
        nbPCommit = commits.filter(commit => commit.oid == commits[i].nbParentOid)[0]
        varPCommit = commits.filter(commit => commit.oid == commits[i].parentOid)[0]
        if (varPCommit!= undefined){
            commit.belongVarBranchIds.forEach((branchID)=>{
                varPCommit.belongVarBranchIds.add(branchID)
            })
        }
        if(nbPCommit!=undefined){
            commit.belongCodeBranchIds.forEach((branchID) => {
                nbPCommit.belongCodeBranchIds.add(branchID)
            })
        }
    }
}

export function parseFilteredCommitIDs(json: any): string[] {
    logger.warn("filtered commit from backend",json)
    return json["commit_ids"]
}
