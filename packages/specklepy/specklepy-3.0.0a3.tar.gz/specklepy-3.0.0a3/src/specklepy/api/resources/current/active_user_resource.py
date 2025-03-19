from typing import List, Optional

from specklepy.core.api.inputs.user_inputs import UserProjectsFilter, UserUpdateInput
from specklepy.core.api.models import (
    PendingStreamCollaborator,
    Project,
    ResourceCollection,
    User,
)
from specklepy.core.api.resources import ActiveUserResource as CoreResource
from specklepy.logging import metrics


class ActiveUserResource(CoreResource):
    """API Access class for users. This class provides methods to get and update
    the user profile, fetch user activity, and manage pending stream invitations."""

    def __init__(self, account, basepath, client, server_version) -> None:
        super().__init__(
            account=account,
            basepath=basepath,
            client=client,
            server_version=server_version,
        )
        self.schema = User

    def get(self) -> Optional[User]:
        metrics.track(metrics.SDK, self.account, {"name": "Active User Get"})
        return super().get()

    def update(
        self,
        input: UserUpdateInput,
    ) -> User:
        metrics.track(metrics.SDK, self.account, {"name": "Active User Update"})

        return super().update(input=input)

    def get_projects(
        self,
        *,
        limit: int = 25,
        cursor: Optional[str] = None,
        filter: Optional[UserProjectsFilter] = None,
    ) -> ResourceCollection[Project]:
        metrics.track(metrics.SDK, self.account, {"name": "Active User Get Projects"})
        return super().get_projects(limit=limit, cursor=cursor, filter=filter)

    def get_project_invites(self) -> List[PendingStreamCollaborator]:
        metrics.track(
            metrics.SDK, self.account, {"name": "Active User Get Project Invites"}
        )
        return super().get_project_invites()
