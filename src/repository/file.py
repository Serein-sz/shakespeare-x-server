from sqlalchemy import select

from src.database import Session
from src.entity import FileTreeCreate, FileTreeDb, FileTreeVo


async def create_file(file: FileTreeCreate) -> None:
    async with Session() as session:
        session.add(FileTreeDb.from_create(file))
        await session.commit()


async def delete_file(id: str) -> None:
    async with Session() as session:
        file = await session.get(FileTreeDb, id)
        if file:
            await session.delete(file)
            await session.commit()


async def update_content(id: str, content: str) -> None:
    async with Session() as session:
        file = await session.get(FileTreeDb, id)
        if file:
            file.content = content
            await session.commit()


async def get_file_content_by_id(id: str) -> str:
    async with Session() as session:
        file = await session.get(FileTreeDb, id)
        return file.content


async def get_files_vo(user_id: str) -> list[FileTreeVo]:
    async with Session() as session:
        result = await session.execute(
            select(FileTreeDb).where(FileTreeDb.user_id == user_id)
        )
        files = result.scalars().all()
        files = map(FileTreeDb.to_tree_node_vo, files)
        children_dict: dict[str, list[FileTreeVo]] = {}
        roots: list[FileTreeVo] = []
        for file in files:
            if file.parent_id is None or file.parent_id == "":
                roots.append(file)
            elif children_dict.get(file.parent_id):
                children_dict[file.parent_id].append(file)
            else:
                children_dict[file.parent_id] = [file]

        def build_tree(nodes: list[FileTreeVo]):
            for node in nodes:
                node.children = children_dict.get(node.id, [])
                build_tree(node.children)

        build_tree(roots)
        return roots
