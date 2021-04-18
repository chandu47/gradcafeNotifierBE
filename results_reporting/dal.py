from database.model.result import ProgramResult, UniResult
from exceptions.result_exception import ResultException
from database.model.user import UserSettings, User
from app import app


class ProgramUpdatesDAL:

    @staticmethod
    def getProgramUpdates(deviceId):
        try:
            # Get the user with the deviceId
            user = User.objects(deviceId=deviceId).first()

            if user is None:
                raise ResultException("No user found exception - {}".format(deviceId))
            # Iterate over the settings and add the program to a map
            all_updates = []
            subscribed_programs = user.program_commit_info
            for programInfo in subscribed_programs:
                programUpdates = ProgramResult.get_program_results_after_commit(programInfo.program, programInfo.last_fetch_commit)
                if len(programUpdates) > 0:
                    combinedProgramUpdate = ProgramUpdatesDAL.combine_program_updates(programUpdates)
                    programInfo.last_fetch_commit = combinedProgramUpdate.latest_commit
                    all_updates.append(combinedProgramUpdate)

            # Combine the results and make the response
            userSettingsDict = {}
            for programSetting in user.settings.selectedPrograms:
                if(programSetting.program not in userSettingsDict):
                    userSettingsDict[programSetting.program] = []
                userSettingsDict[programSetting.program].append(programSetting)

            all_updates = ProgramUpdatesDAL._filter_out_updates(all_updates, userSettingsDict)

            #Update last_fetch_commit info in user commitInfo
            user.save()

            return all_updates
        except Exception as ex:
            app.logger.error(ex)
            app.logger.error("Oops Something looks fishy here.")
            raise ResultException("Exception while fetching User Info - {}".format(deviceId))


        #Update the commits

    @staticmethod
    def _filter_out_updates(updates, settings):
        for update in updates:
            newUpdatesListt = []
            for setting in settings[update.program]:
                for pro in update.universities: ##Optimize better than from O(n^2)
                    if pro.university == setting.university and pro.season == setting.season and pro.degree == pro.degree and pro.commit_id>setting.last_fetch_commit:
                        newUpdatesListt.append(pro)

                ##Update last_fetch_commit or last_seen_commit for each setting
                setting.last_fetch_commit = update.latest_commit

            update.universities = newUpdatesListt

        updates = [update for update in updates if len(update.universities)>0]
        return updates

    @staticmethod
    def combine_program_updates(updatesList):
        #The first item in list is the base because sorted based on commit
        programUpdate = updatesList[0]

        for index in range(1, len(updatesList)):
            programUpdate.universities.extend(updatesList[index].universities)

        return programUpdate



