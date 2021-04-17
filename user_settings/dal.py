from database.model.user import User, UserSettings, Program, ProgramCommitInfo
from database.model.program import Program as ProgramCol
from database.model.university import University as UniCol
from main import app
from exceptions.user_settings_exception import UserSettingsException

class UserSettingsDAL:

    @staticmethod
    def getAllSettingsForUser(deviceId) -> UserSettings:
        try:
            target = User.objects(deviceId=deviceId).first()
        except Exception as ex:
            app.logger.error(ex)
            app.logger.error("Oops Something looks fishy here.")
            raise UserSettingsException("Exception while fetching User Info - {}".format(deviceId))
        if target is not None:
            return target.settings
        else:
            raise UserSettingsException("No User with deviceId - {}".format(deviceId))

    @staticmethod
    def addSettingsForUser(deviceId, requestData) -> UserSettings:
        try:
            user = User.objects(deviceId=deviceId).first()
            if user:
                print(user.settings.selectedPrograms)
                UserSettingsDAL._mapUserSettingsDictToEntity(requestData, user)
                user.save()
                return user.settings
            else:
                app.logger.error("No user found")
                raise UserSettingsException("No user found with deviceId - {}".format(deviceId))

        except UserSettingsException as ex:
            app.logger.error(ex)
            raise ex

        except Exception:
            app.logger.error("Oops Something looks fishy here.")
            raise UserSettingsException("Exception while fetching User Info - {}".format(deviceId))

    @staticmethod
    def getOneSettingForUser(deviceId, settingId):
        try:
            target = User.objects(deviceId=deviceId).first()
        except:
            app.logger.error("Oops Something looks fishy here.")
            raise UserSettingsException("Exception while fetching User Info - {}".format(deviceId))
        if target is not None:
            data = target.settings.get_setting(settingId)
            if data is not None:
                return data
            else:
                raise UserSettingsException("No User with deviceId - {} and settingId - {}".format(deviceId, settingId))
        else:
            raise UserSettingsException("No User with deviceId - {}".format(deviceId))

    @staticmethod
    def updateOneSettingForUser(deviceId, settingId, reqData):
        try:
            target = User.objects(deviceId=deviceId).first()
        except:
            app.logger.error("Oops Something looks fishy here.")
            raise UserSettingsException("Exception while fetching User Info - {}".format(deviceId))
        if target is not None:
            program = target.settings.get_setting(settingId)
            oldProg = program.program
            oldUni = program.university
            newProg = reqData['program']
            newUni = reqData['university']
            if program is not None:
                program.program = reqData['program']
                program.university = reqData['university']
                program.season = reqData['season']
                program.degree = reqData['degree']
                if target.settings.check_dup(program):
                    raise UserSettingsException("Duplicate Setting already exists.")

                resetLastFetchCounter = False
                #Update the counters
                if not oldProg == newProg:
                    UserSettingsDAL._updateProgramCounter(oldProg, target, False)
                    UserSettingsDAL._updateProgramCounter(newProg, target, True)
                    resetLastFetchCounter = True

                if not oldUni == newUni:
                    UserSettingsDAL._updateUniversityCounter(oldUni, False)
                    UserSettingsDAL._updateUniversityCounter(newUni, True)

                #Reset last_fetch_commit if not already reset
                if not resetLastFetchCounter:
                    commitInfo = target.has_program(newProg)
                    if commitInfo is not None:
                        commitInfo.last_fetch_commit= -1

                #Reset the settings last fetch counter
                program.last_fetch_commit = -1

                target.save()
                return program
            else:
                raise UserSettingsException("No User with deviceId - {} and settingId - {}".format(deviceId, settingId))
        else:
            raise UserSettingsException("No User with deviceId - {}".format(deviceId))

    @staticmethod
    def updateSettingsForUser(deviceId, reqData):
        try:
            target = User.objects(deviceId=deviceId).first()
            if target is not None:
                settings = target.settings
                if 'enableRejectNotifs' in reqData:
                    settings.enableRejectNotifs = reqData['enableRejectNotifs']

                if 'enableInfoNotifs' in reqData:
                    settings.enableInfoNotifs = reqData['enableInfoNotifs']

                target.save()
                return target.settings;
            else:
                app.logger.error("No User with deviceId - {}".format(deviceId))
                raise UserSettingsException("No User with deviceId - {}".format(deviceId))
        except UserSettingsException as ex:
            raise ex
        except:
            app.logger.error("Oops Something looks fishy here.")
            raise UserSettingsException("Exception while fetching or updating User Info - {}".format(deviceId))



    @staticmethod
    def removeOneSettingForUser(deviceId, settingId):
        try:
            target = User.objects(deviceId=deviceId).first()
            if target is not None:
                data = target.settings.get_setting(settingId)
                if data is not None:
                    UserSettingsDAL._updateUniversityCounter(data.university, False)
                    UserSettingsDAL._updateProgramCounter(data.program, target, False)
                    target.settings.selectedPrograms.remove(data)
                    target.save()
                    return target.settings
                else:
                    raise UserSettingsException("No User with deviceId - {} and settingId - {}".format(deviceId, settingId))
            else:
                raise UserSettingsException("No User with deviceId - {}".format(deviceId))
        except UserSettingsException as ex:
            app.logger.error(ex.message)
            raise ex
        except Exception:
            app.logger.error("Oops Something looks fishy here.")
            raise UserSettingsException("Exception while fetching User Info - {}".format(deviceId))

    @staticmethod
    def _mapUserSettingsDictToEntity(reqData, user):
        newSettingId = -1
        for settingReq in reqData['selectedPrograms']:
            # Get highest settingId in current settings list
            ##Create new Setting
            program = Program()
            program.program = settingReq['program']
            program.university = settingReq['university']
            program.season = settingReq['season']
            program.degree = settingReq['degree']
            if newSettingId < 0:
                for setting in user.settings.selectedPrograms:
                    newSettingId = max(newSettingId, setting.settingId)
                    if(program==setting):
                        raise UserSettingsException("Duplicate Setting already exists.")

            newSettingId+=1
            UserSettingsDAL._updateProgramCounter(program.program, user, True)
            UserSettingsDAL._updateUniversityCounter(program.university, True)

            program.settingId = newSettingId
            user.settings.selectedPrograms.append(program)





    @staticmethod
    def _updateProgramCounter(progEntry, user, isInc):
        # Increment programcounters
        try:
            programEntity = ProgramCol.objects(program=progEntry).first()
            if programEntity is not None:
                if isInc:
                    programEntity.count += 1


                elif programEntity.count > 0:
                    programEntity.count -= 1


                programEntity.save()

            UserSettingsDAL._updateProgramCommitInfo(progEntry, user, isInc)
        except Exception as ex:
            raise UserSettingsException("Error while updating program and university counters" + ex)


    @staticmethod
    def _updateProgramCommitInfo(progEntry, user, isInc):
        commitInfo = user.has_program(progEntry)
        if commitInfo is None and not isInc:
            raise UserSettingsException("Error: Did not find program in commitInfo - {}".format(progEntry))


        if isInc and commitInfo is None:
            newProgramCommit = ProgramCommitInfo()
            newProgramCommit.program = progEntry
            newProgramCommit.count = 1
            user.program_commit_info.append(newProgramCommit)

        elif isInc:
            commitInfo.count += 1
            commitInfo.last_fetch_commit = -1

        elif commitInfo.count > 1:
            commitInfo.count -= 1

        else:
            user.program_commit_info.remove(commitInfo)

    @staticmethod
    def _updateUniversityCounter(uniEntry, isInc):
        try:
            uniEntity = UniCol.objects(university=uniEntry).first()
            if uniEntity is not None:
                if isInc:
                    uniEntity.count += 1
                elif uniEntity.count > 0:
                    uniEntity.count -= 1
                uniEntity.save()
        except:
            raise UserSettingsException("Error while updating program and university counters")

