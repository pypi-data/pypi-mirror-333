import json
import rich

class Kanapka:
    test: int = 1
    anoga: int = 2

    def noga(self):
        print("but !!! change!!!!!!!!!")

    def noga2(self):
        print("but change! changing here!!!")

    def dodaje(self, kupa):
        print(f"but change! changing here!!")
        print("HEH!!!!!")

        print("A@!!WINDOW !!! LIFE!!!!! !!!!!!!!!!!!!!!!!!!!")
        print("!!!!THIRD!!!")
        print("!!!!!!SECOND!!")


@rx.event
def test0():
    print("ABC23333!!!yyyyyy ## !!!")
    b = ['1', '2', '3']
    for a in b:
        print(f"BBBB{a}")


def test():
    pass # wild snakes !



class BasePythonMethodProcessor:

    @rx.event
    def update_current_answers(self, current_answers: Dict[str, Any]) -> bool:
        """
        Updates !!!! current !! answers based on data from API!!!!!@@@@@@@22222234343434 ###
        """
        logger.debug(f'Updating current answers with: {current_answers} !!')
        self.current_answers = current_answers

async def test2(results: List[PatchResult], approvals: Dict[str, bool]) -> int:
    """
    Applies approved changes to files.

    Args:
        results: List of operation results
        approvals: Dictionary with approval decisions

    Returns:
        int: Number of modified files
    """
    modified_count = 0
    for result in results:
        if approvals.get(result.path, False):
            try:
                if result.should_delete:
                    # Delete the file instead of writing empty content
                    if os.path.exists(result.path):
                        os.remove(result.path)
                        console.print(f'[green]Deleted file: {result.path}[/green]')
                        modified_count += 1
                    else:
                        console.print(f'[yellow]File does not exist: {result.path}[/yellow]')
                else:
                    # Standard content writing
                    directory = os.path.dirname(result.path)
                    if directory:
                        os.makedirs(directory, exist_ok=True)
                    with open(result.path, 'w', encoding='utf-8') as f:
                        f.write(result.current_content)
                    console.print(f'[green]Applied changes to {result.path}[/green]')
                    modified_count += 1
            except Exception as e:
                console.print(f'[bold red]Error applying changes to {result.path}: {e}[/bold red]')
    return modified_count

